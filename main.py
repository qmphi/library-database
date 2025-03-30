import library_Funcs as A
#main menu
def main_menu():
    menu = """\nWelcome to the library!
To navigate, please use the following instructions:

  1 - Browse 
  2 - To return an item
  3 - View library events
  4 - Donate an item
  5 - Apply for volunteering
  6 - Help
  0 - Exit the program
    """
    print(menu)

userInput = -1

while (userInput != 0):

    main_menu()
    userInput = int(input("I want to navigate to: "))
    if (userInput == 1): #Browse items
        A.borrowItem()
        #--> can search by different filters (id, genre, type etc)
            #-->prompt user if they want to borrow, ask for userID. 
                #--> If no userID, prompt new user?
        continue
    elif (userInput == 2): #Manage loans (return and item info/fines)
        userID = int(input("Please enter your userID to continue:" ))
        A.manageLoans(userID)
        continue
    elif (userInput == 3): #View library events
        A.viewEvents()
        continue
    elif (userInput == 4): #Donate an item
        continue
    elif (userInput == 5): # Apply for volunteering
        A.applyVolunteer()
        continue
    elif (userInput == 6): #Help
        A.askLibrarian()
        continue
    elif (userInput == 0): #Exit program
        break
    else:
        print("Invalid menu code, please try again")






