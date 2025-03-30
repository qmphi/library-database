import sqlite3
from datetime import datetime, timedelta 

database = 'library.db'

# #func for dealing with connections
# isWrite is for any writing operations 0 if no, 1 if yes
def databaseConnector(database, query, params, isWrite):
    try:
        with sqlite3.connect(database) as conn:
            if isWrite == 0:
                cursor = conn.cursor()
                cursor.execute(query, params)
                items = cursor.fetchall()
                return items
            else:
                cursor = conn.cursor()
                cursor.execute(query, params)
                items = cursor.fetchall()
                conn.commit()
    except sqlite3.OperationalError as e:
        print(e)
        return []

def browseItems():
    print("\nAvailable items in the library:")

    #filters:
    author_filter = input("Enter an author's full name to filter by (or press Enter to skip): ")
    publicationYear_filter = input("Enter a publication year to filter by (or press Enter to skip): ")
    itemType_filter =input("Enter an item type to filter by (or press Enter to skip): ").strip()
    genre_filter = input("Enter a genre to filter by (or press Enter to skip): ").strip()
    
    query = "SELECT itemID, title, author, genre FROM item WHERE isAvailable = 1 "
    params = []

    #dynamically add filters
    if author_filter:
        query += "AND author LIKE ?"
        params.append(f"%{author_filter}%")
    if publicationYear_filter:
        query += "AND publicationYear = ?"
        params.append(int(publicationYear_filter))
    if itemType_filter:
        query += "AND itemType LIKE ?"
        params.append(f"%{itemType_filter}%")
    if genre_filter:
        query += "AND genre LIKE ?"
        params.append(f"%{genre_filter}%")
    # print("Generated Query: ", query)
    # print("Query Parameters: ", params)
    returnedItems = databaseConnector(database, query, params, 0) #it's a reading operation
    if not returnedItems:
        print("No matches found")
        return
   
    #display list
    for item in returnedItems:
         print(f"{item[0]}. {item[1]} by {item[2]} (Genre: {item[3]})") 

    #borrow input
    itemID = int(input("\nEnter the item ID to of the item you want to borrow:"))
    query = "SELECT title FROM item WHERE isAvailable = 1 AND itemID = ?"
    params = [itemID]
    checkItemID = databaseConnector(database, query, params, 0)

    if checkItemID:
        userID = int(input("\nTo borrow an item, please enter your userID or if you do not have one, enter 0: "))
        if (userID != 0):# has a userID
            borrowItem(itemID, userID)
        else: #need to add new user
            firstName = input("\nPlease enter your first name: ").split()
            lastName = input("\nPlease enter your last name: ").split()
            phoneNum = int(input("\nPlease enter your phone number (no spaces): "))
            newUserID = addUser(firstName, lastName, phoneNum)
            borrowItem(itemID, newUserID)
    else:
        print("This itemID is not valid or the item is not available")


#add ID systematically

def addUser(firstName, lastName, phoneNum):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        insertStatement = """
            INSERT INTO patron (firstName, lastName, phoneNum)
            VALUES (?, ?, ?);
        """
        try:
            cursor.execute(insertStatement, (firstName, lastName, phoneNum))
            conn.commit()
            userId = cursor.lastrowid
            print("User created successfully!")
            print("Your userID is: " + str(userId))
            return userId # changed to return userID so can use if needed
          
        except sqlite3.Error as e:
            print("Error:", e)
            return None

    
def borrowItem(itemID, userID):
    query = "SELECT title FROM item WHERE isAvailable = 1 AND itemID = ?"
    params = [itemID]
    item = databaseConnector(database, query, params, 0)
    if item:
        #add new borrowedBy entry
        borrowDate = datetime.today().strftime('%Y-%m-%d')
        dueDate = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')
        insertQuery = "INSERT INTO borrowedBy (itemID, userID, borrowDate, dueDate, returnDate) VALUES (?, ?, ?, ?, NULL)"
        insertParams = [itemID,userID,borrowDate, dueDate]
        databaseConnector(database, insertQuery, insertParams, 1)

        #update item isAvailable status
        updateQuery = "UPDATE item SET isAvailable = 0 WHERE itemID = ?"
        updateParam = (itemID,)
        databaseConnector(database, updateQuery, updateParam, 1)

        print(f"\nYou borrowed {item[0]}. Please return it by {dueDate}.")
    else:
        print("Item is not available for borrowing")

        
def returnItem(itemID, userID):
    query = "SELECT title FROM item WHERE isAvailable = 0 AND itemID = ?"
    params = [itemID]
    item = databaseConnector(database, query, params, 0)
    if item:
        #check overdue days and calc fine amnt
        dueDate = item[1]
        dueDateObj = datetime.strptime(dueDate, '%Y-%m-%d')
        returnDateObj = datetime.strptime(returnDate, '%Y-%m-%d')
        overdueDays = (returnDateObj - dueDateObj).days

        fineAmnt = 0.0
        if overdueDays > 0:
            fineAmnt = overdueDays * 2.0 #random due date amnt of $2 per day
            print(f"This item is {overdueDays} days overdue. A fine of {fineAmnt:.2f} has been applied.")

        #update borrowedBy table
        returnDate = datetime.today().strftime('%Y-%m-%d')
        insertQuery = "UPDATE borrowedBy SET returnDate = ?, fineAmnt = ? WHERE itemID = ? AND userID = ?"
        insertParams = [returnDate, fineAmnt, itemID, userID]
        databaseConnector(database, insertQuery, insertParams, 1)

        #update in item table, set isAvailable to 1
        updateReturnedQuery = "UPDATE item SET isAvailable = 1 WHERE itemID = ?" 
        updateParam = [itemID]
        databaseConnector(database, updateReturnedQuery, updateParam, 1) 
        print(f"\nYou have returned {item[0]}. Thank you!.")
    else:
        print("You have not borrowed this item")

def manageLoans(userID):
    query = "SELECT userID FROM patron WHERE userID = ?"
    params = (userID,)
    patron = databaseConnector(database, query, params, 0)
    navigationCtrl = -1

    if patron:
        while navigationCtrl != 0:
            print("Here are your current loans")
            patronItemQuery = "SELECT i.itemID, i.title, i.author, i.itemType, b.borrowDate, b.dueDate FROM item AS i JOIN borrowedBy AS b ON b.itemID = i.itemID JOIN patron AS p ON p.userID = b.userID WHERE p.userID = ? AND i.isAvailable = 0" 
            itemParams = (userID,)

            items = databaseConnector(database, patronItemQuery, itemParams, 0) #it's a reading operation
            if not items:
                print("No current loans")
                return
        
            #display list
            for item in items:
                print(f"{item[0]}. {item[1]} by {item[2]} {item[3]} borrowed: {item[4]} due: {item[5]})")
                    
            returnItemID = int(input("If you would like to return a loan, please enter the itemID (press enter to skip): "))
            if returnItemID:
                returnItem(returnItemID, userID)
            
            navigationCtrl = int(input("To exit Managing loans, press 0: "))


    else:
        print("\nYou currently do not have an existing userID, please create a new one")
        firstName = input("\nPlease enter your first name: ").split()
        lastName = input("Please enter your last name: ").split()
        phoneNum = int(input("Please enter your phone number (no spaces): "))
        addUser(firstName, lastName, phoneNum)
        #kick them back to main menu because can't borrow without an id and they just made one

    