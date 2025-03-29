import sqlite3

database = 'library.db'

#reminder need to open and close db connection in each 
def browseItems():
    return None

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
    return None
def returnItem(itemID, userID):
    return None

