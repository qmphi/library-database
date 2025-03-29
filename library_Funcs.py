import sqlite3

database = 'library.db'

#reminder need to open and close db connection in each 
#func for dealing with connections
#isWrite is for any writing operations 0 if no, 1 if yes
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
        # if itemID:
            #borrowItems
    # else:
    #     #add user Func here
    #     itemID = int(input("\nEnter the item ID to borrow or press Enter to go back:"))
    #     if itemID:
    #         #borrowItems
    #         break



    

#add ID systematically
# def addUser(firstName, lastName, phoneNum):
    
def borrowItem(itemID, userID):
    # query = "SELECT itemID, title, genre FROM item WHERE isAvailable = 1
    # databaseConnector(database, query, params, isWrite)
    
# def returnItem(itemID, userID):
    

