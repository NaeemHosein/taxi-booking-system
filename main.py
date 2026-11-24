from database import DatabaseManager, DuplicateAccountError
from pwinput import pwinput
from email_validator import validate_email, EmailNotValidError


MENU = """
Welcome User
Please indicate your selection by choosing the appropriate number from the list below.
1) Login
2) Register
3) Quit

Enter: 
"""

CONFIRM_REGISTER_MENU = """
Welcome to the registration screen.
Please select the appropriate option.
1) Continue
2) Back

Enter: 
"""



def get_new_email(db: DatabaseManager):
    while True:
        email = input("Enter your email address: ")
        try:
            validate_email(email, check_deliverability=False)
            
        except EmailNotValidError:
            print(f"Invalid email. Please try again")
            continue
        if db.email_exists(email):
            print("Email already registered. Please try again")
            continue
        print("Email available.")
        return email

def get_new_password():
    while True:
        password = pwinput("Enter your password: ")
        confirmed_password = pwinput("Confirm password: ")
        if password == confirmed_password:
            return password
        else:
            print("Password does not match. Please try again")
        


def login(db: DatabaseManager):
    while True:
        email = input("Please enter your email: ")
        password = input("Please enter your password: ")
        user = db.authenticate(email, password)
        if user is None:
            print("Invalid credientials.")
        else:
            user.view_dashboard()
            #Fix this and see how it flows.
            break
        #We have to add a way for them to go back to the main menu if they dont want to login

def confirm_registration(db : DatabaseManager):
    while True:
        choice = input(CONFIRM_REGISTER_MENU)
        if choice == "1":
            register(db)
        elif choice == "2":
            return
        else:
            print("Invalid input.\nPlease indicate your selection by choosing the appropriate number from the list")
            continue

def register(db: DatabaseManager):
        
    print("Please enter the correct registration information below.")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    address = input("Enter your address: ")
    #Phone suppose to be unique and no one else should have the same phone number
    phone = input("Enter your phone number: ")
    email = get_new_email(db)
    password = get_new_password()

    try:
        
        db.register_customer(first_name, last_name, email, password, phone, address)
        print("Registration Successful.")
    except DuplicateAccountError as error:
        print(error)
    #Put a way to cancel while registering to go back to main menu





def main():
    db = DatabaseManager("taxi_booking.db")
    try:
        run_program(db)

    finally:
        db.close()
    




def run_program(db: DatabaseManager):
    while True:
        choice = input(MENU)
        if choice in starting_menu:
            starting_menu[choice](db)

        
        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid Input. Please try again")
            continue 

            





starting_menu = {
    "1" : login,
    "2" : confirm_registration
}









if __name__ == "__main__":
    main()


