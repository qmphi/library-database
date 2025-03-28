#main menu
def main_menu():
    menu = """\nWelcome to the library!
To navigate, please use the following instructions:

  1 - Browse items
  2 - To borrow an item
  3 - To return an item
  4 - View library events
  5 - Donate an item
  6 - Apply for volunteering
  7 - Help
  0 - Exit the program
    """
    print(menu)

userInput = -1

while (userInput != 0):
    ##if not logged in, can't borrow, return, register for events##

    main_menu()
    userInput = int(input("I want to navigate to: "))
    if (userInput == 1): #Browse items
        #--> can search by different filters
        #searchFunc
        continue
    elif (userInput == 2): #borrow an item
        continue
    elif (userInput == 3): #return an item
        continue
    elif (userInput == 4): #View library events
        #View events --> can filter by audience, type, time, etc
        # register for event
        continue
    elif (userInput == 5): #Donate an item
        continue
    elif (userInput == 6): # Apply for volunteering
        continue
    elif (userInput == 7): #Help
        continue
    elif (userInput == 0): #Exit program
        break
    else:
        print("Invalid menu code, please try again")






