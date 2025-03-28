#main menu
def main_menu():
    menu = """\nWelcome to the library!
To navigate, please use the following instructions:

  1 - Browse items
  2 - Log in (for staff, volunteers, and users)
  3 - View library events
  4 - Donate an item
  5 - Apply for volunteering
  6 - Help
  0 - Exit the program
    """
    print(menu)

userInput = -1

while (userInput != 0):
    ##if not logged in, can't borrow, return, register for events##

    main_menu()
    userInput = int(input("I want to navigate to: "))
    if (userInput == 1):
        #--> can search by different filters
        #searchFunc
        continue
    elif (userInput == 2):
        # view my books 
        # return book
        # can continue browsing, just can't borrow
        continue
    elif (userInput == 3):
        #View events --> can filter by audience, type, time, etc
        # register for event
        continue
    elif (userInput == 4):
        continue

    elif (userInput == 5):
        continue

    elif (userInput == 6):
        continue

    elif (userInput == 0):
        break
    else:
        print("Invalid menu code, please try again")






