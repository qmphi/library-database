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
            print("New user created with userID: " + str(userId))
            return userId
          
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


def viewEvents():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        print("\nAll available events: ")

        # Get filters from the user
        eventType_filter = input("Enter an event type to filter by (or press Enter to skip): ").strip()
        eventDate_filter = input("Enter a date (YYYY-MM-DD) to filter by (or press Enter to skip): ").strip()
        startTime_filter = input("Enter a starting time to filter by (or press Enter to skip): ").strip()

        query = "SELECT eventID, eventName, eventType, eventDate, startTime, endTime FROM events WHERE 1=1"
        params = []

        if eventType_filter:
            query += " AND eventType = ?"
            params.append(eventType_filter)
        if eventDate_filter:
            query += " AND eventDate = ?"
            params.append(eventDate_filter)
        if startTime_filter:
            query += " AND startTime = ?"
            params.append(startTime_filter)

        cursor.execute(query, tuple(params))
        events = cursor.fetchall()

        if not events:
            print("No matching events found.")
            return None

        print("\nAvailable Events:")
        print("-" * 50)
        event_map = {}
        for event in events:
            eventID, eventName, eventType, eventDate, startTime, endTime = event
            event_map[eventID] = eventName
            print(f"ID: {eventID} | {eventName} ({eventType}) on {eventDate} from {startTime} to {endTime}")

        while True:
            try:
                register = input("Would you like to register for an event? (Y/N) ").strip().upper()

                if register == "Y":
                    selected_id = int(input("\nEnter the event ID you want to register for (Enter 0 to go back to main menu): "))
                    if selected_id == 0:
                        return None

                    cursor.execute("SELECT eventID FROM events WHERE eventID = ?", (selected_id,))
                    if cursor.fetchone():
                        while True:
                            user_input = input("Enter your userID (Enter 0 to return to Main Menu or press Enter to create a new user): ").strip()
                            if user_input == "":
                                print("No userID entered. Creating new user.\n")
                                fname = input("Enter your first name: ").strip()
                                lname = input("Enter your last name: ").strip()
                                phoneNum = input("Enter your phone number: ").strip()
                                userID = addUser(fname, lname, phoneNum)
                                break
                            elif user_input == "0":
                                return None
                            else:
                                try:
                                    userID = int(user_input)
                                    cursor.execute("SELECT userID FROM patron WHERE userID = ?", (userID,))
                                    if cursor.fetchone():
                                        break
                                    else:
                                        print("UserID not found. Please try again (0 to return to Main Menu) or press Enter to create a new user.")
                                except ValueError:
                                    print("Invalid userID entered. Please try again or press Enter to create a new user.")

                        try:
                            cursor.execute(
                                "INSERT INTO registerEvent (eventID, userID) VALUES (?, ?)", (selected_id, userID)
                            )
                            conn.commit()
                            eventName = event_map.get(selected_id, "the event")
                            print(f"Registration Successful! You're now registered for {eventName}.\n")
                            print("Returning to Main Menu.\n")
                            return selected_id
                        except sqlite3.IntegrityError:
                            print("Registration failed: You may have already registered for this event or provided an invalid userID.\n")
                            return None
                    else:
                        print("Invalid event ID. Please try again.\n")
                else:
                    return None

            except ValueError:
                print("Invalid input. Please enter a valid event ID.\n")


def applyVolunteer():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        print("\nVolunteer Application")
        
        user_input = -1
        # Get or create a patron account
        while True:
            user_input = input("Enter your userID (Enter 0 to return to Main Menu or press Enter to create a new user): ").strip()
            if user_input == "":
                print("No userID entered. Creating new account.\n")
                fname = input("Enter your first name: ").strip()
                lname = input("Enter your last name: ").strip()
                phoneNum = input("Enter your phone number: ").strip()
                userID = addUser(fname, lname, phoneNum)
                break
            if user_input == "0":
                print("Returning to Main Menu.\n")
                return None    
            else:
                try:
                    userID = int(user_input)
                    cursor.execute("SELECT userID, firstName, lastName, phoneNum FROM patron WHERE userID = ?", (userID,))
                    row = cursor.fetchone()
                    if row:
                        break
                    else:
                        print("UserID not found. Please try again or press Enter to create a new account.")
                except ValueError:
                    print("Invalid input. Please enter a valid numeric userID or press Enter to create a new account.")
        
        # Retrieve patron details (for an existing user)
        cursor.execute("SELECT firstName, lastName, phoneNum FROM patron WHERE userID = ?", (userID,))
        patron_data = cursor.fetchone()
        if not patron_data:
            print("Patron record not found. Aborting.")
            return
        fname, lname, phoneNum = patron_data
        
        position = "Volunteer"
        isActive = 1 
        
        try:
            cursor.execute(
                "INSERT INTO personnel (firstName, lastName, POSITION, phoneNum, isActive) VALUES (?, ?, ?, ?, ?)",
                (fname, lname, position, phoneNum, isActive)
            )
            conn.commit()
            new_staffID = cursor.lastrowid
            
            # Insert the record in the volunteers table linking the patron to the new personnel record
            cursor.execute(
                "INSERT INTO volunteers (userID, staffID) VALUES (?, ?)",
                (userID, new_staffID)
            )
            conn.commit()
            print("Application successful! You're now a Volunteer, you're staffID is :" + str(new_staffID))
        except sqlite3.IntegrityError as e:
            print("Application failed:", e)


def askLibrarian():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        print("\nAsk a Librarian")
        
        # Get or create a patron account
        while True:
            user_input = input("Enter your userID (enter 0 to return to Main Menu, or press Enter to create a new account): ").strip()
            if user_input == "0":
                print("Returning to Main Menu.\n")
                return None
            if user_input == "":
                print("No userID entered. Creating new account.\n")
                fname = input("Enter your first name: ").strip()
                lname = input("Enter your last name: ").strip()
                phoneNum = input("Enter your phone number: ").strip()
                userID = addUser(fname, lname, phoneNum)
                break
            else:
                try:
                    userID = int(user_input)
                    cursor.execute("SELECT userID FROM patron WHERE userID = ?", (userID,))
                    if cursor.fetchone():
                        break
                    else:
                        print("UserID not found. Please try again or press Enter to create a new account.")
                except ValueError:
                    print("Invalid input. Please enter a valid numeric userID, 0 to return to Main Menu, or press Enter to create a new account.")
        
        description = input("Enter a description of your request: ").strip()
        if not description:
            print("Request description cannot be empty. Aborting.")
            return None
        
        cursor.execute("SELECT staffID, firstName, lastName FROM personnel WHERE POSITION = 'Librarian' AND isActive = 1")
        librarians = cursor.fetchall()

        if not librarians:
            print("No active librarian found. Please try again later.")
            return None
        
        if len(librarians) > 1:
            print("\nAvailable Librarians:")
            for staffID, firstName, lastName in librarians:
                print(f"Staff ID: {staffID} - {firstName} {lastName}")

            while True:
                try:
                    selected_staffID = int(input("Enter the Staff ID of the librarian you want to ask: ").strip())
                    if any(staffID == selected_staffID for staffID, _, _ in librarians):
                        staffID = selected_staffID
                        break
                    else:
                        print("Invalid Staff ID. Please select from the list above.")
                except ValueError:
                    print("Invalid input. Please enter a valid numeric Staff ID.")

        else: #only 1 librarian avail
            staffID = librarians[0][0]
            print(f"Automatically assigned to Librarian: {librarians[0][1]} {librarians[0][2]} (Staff ID: {staffID})")


        requestTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status = 0

        try:
            cursor.execute(
                "INSERT INTO askLibrarian (userID, staffID, requestTime, description, status) VALUES (?, ?, ?, ?, ?)",
                (userID, staffID, requestTime, description, status)
            )
            conn.commit()
            print("Your request has been submitted successfully!")
        except sqlite3.IntegrityError as e:
            print("Failed to submit your request:", e)
