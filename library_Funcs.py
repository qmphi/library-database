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
        print("here")
        print(e)
        return []

def browseItems():
    print("\nAvailable items in the library:")

    #filters:
    # author_filter = input("Enter an author's full name to filter by (or press Enter to skip): ").strip()
    publicationYear_filter = input("Enter a publication year to filter by (or press Enter to skip): ")
    itemType_filter =input("Enter an item type to filter by (or press Enter to skip): ").strip()
    genre_filter = input("Enter a genre to filter by (or press Enter to skip): ").strip()
    
    query = "SELECT itemID, title, genre FROM item WHERE isAvailable = 1 "
    params = []

    #dynamically add filters
    # if author_filter:
    #     query += "AND author LIKE ?"
    #     params.append(f"%{author_filter}%")
    if publicationYear_filter:
        query += "AND publicationYear = ?"
        params.append(int(publicationYear_filter))
    if itemType_filter:
        query += "AND itemType LIKE ?"
        params.append(f"%{itemType_filter}%")
    if genre_filter:
        query += "AND genre LIKE ?"
        params.append(f"%{genre_filter}%")
    print("Generated Query: ", query)
    print("Query Parameters: ", params)
    returnedItems = databaseConnector(database, query, params, 0) #its a reading operation
    if not returnedItems:
        print("No matches found")
        return
   
    #display list
    for item in returnedItems:
         print(f"{item[0]}. {item[1]} (Genre: {item[2]})") #missing author field add back later

    #borrow input
    userID = int(input("\nTo borrow an item, please enter your userID or if you do not have one, enter 1: "))
    if (userID != 1):
        itemID = int(input("\nEnter the item ID to borrow or press Enter to go back:"))
        if itemID:
            borrowItem(itemID, userID)
    # else:
        #add user Func here
        # newUserID = 
        # itemID = int(input("\nEnter the item ID to borrow or press Enter to go back:"))
        # if itemID:
        #     # borrowItem(itemID, newUserID)
        #     break

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
            return None
          
        except sqlite3.Error as e:
            print("Error:", e)
            return None

    
def borrowItem(itemID, userID):
    query = "SELECT title FROM item WHERE isAvailable = 1 AND itemID = ?"
    params = itemID
    item = databaseConnector(database, query, params, 0)
    if item:
        #add new borrowedBy entry
        borrowDate = datetime.today().strftime('%Y-%m-%d')
        dueDate = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')
        insertQuery = "INSERT INTO borrowedBy (itemID, userID, borrowDate, dueDate, returnDate) VALUES (?, ?, ?, ?, NULL)"
        insertParams = [itemID,userID,borrowDate, dueDate, "NULL"]
        databaseConnector(database, insertQuery, insertParams, 1)

        #update item isAvailable status
        updateQuery = "UPDATE item SET isAvailable = 0 WHERE itemID = ?"
        updateParam = itemID
        databaseConnector(database, updateQuery, updateParam, 1)

        print(f"\nYou borrowed '{item[0]}`. Please return it by {dueDate}.")
    else:
        print("Item is not available for borrowing")

        
def returnItem(itemID, userID):
    query = "SELECT title FROM item WHERE isAvailable = 0 AND itemID = ?"
    params = itemID
    item = databaseConnector(database, query, params, 0)
    if item:
        #update borrowedBy table
        returnDate = datetime.today().strftime('%Y-%m-%d')
        insertQuery = "UPDATE borrowedBy SET returnDate ? WHERE itemID = ? AND userID = ?"
        insertParams = [returnDate, item, userID]
        databaseConnector(database, insertQuery, insertParams, 1)

        #update in item table, set isAvailable to 1
        updateReturnedQuery = "UPDATE item SET isAvailable = 1 WHERE itemID = ?" 
        updateParam = itemID
        databaseConnector(database, updateReturnedQuery, updateParam, 1) 
        #TODO if ()#over due case?
        print(f"\nYou returned '{item[0]}`. Thank you!.")
    else:
        print("Item is not available for borrowing")

