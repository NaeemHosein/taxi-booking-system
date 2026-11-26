from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from datetime import date, datetime
from textwrap import dedent
from typing import TYPE_CHECKING
from tabulate import tabulate

if TYPE_CHECKING:
    from database import DatabaseManager


CUSTOMER_DASH = """\
Please indicate your selection by choosing the appropriate number from the list below.
1) Book Taxi
2) View Bookings
3) View Booking History
4) Cancel Booking
5) Logout

Enter: 
"""

DRIVER_DASH = """\
Please indicate your selection by choosing the appropriate number from the list below.
1) View Assigned Bookings
2) Return to login
3) Quit

Enter: 
"""

DRIVER_DASH = """\
Please indicate your selection by choosing the appropriate number from the list below.
1) View Assigned Bookings
2) Return to login
3) Quit

Enter: 
"""

ADMINISTRATOR_DASH = """\
Please indicate your selection by choosing the appropriate number from the list below.
1) Assign Driver
2) Return to login
3) Quit
"""





class BookingStatus(Enum):
    PENDING_DRIVER_ASSIGNMENT = "Pending Driver Assignment"
    DRIVER_ASSIGNED = "Driver Assigned"
    CANCELLED = "Cancelled"


class Booking:
    def __init__(self, booking_id, pick_up, drop_off, start_datetime, status, customer, driver):
        self._booking_id = booking_id
        self._pick_up = pick_up
        self._drop_off = drop_off
        self._start_datetime = start_datetime
        self._status = BookingStatus.PENDING_DRIVER_ASSIGNMENT
        self._customer = customer
        self.driver = None


    def assign_driver(self, driver):
        ...

    def cancel(self):
        ...

class User(ABC):
    def __init__(self, user_id, first_name, last_name, email, password_hash, phone, db: DatabaseManager):
        
        self._user_id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password_hash = password_hash
        self._phone = phone
        self._db = db

    @property
    def user_id(self):
        return self._user_id
    
    def verify_password(self, email, password):
        ...

    def logout(self):
        ...

    @abstractmethod
    def view_dashboard(self):
        ...



class Customer(User):
    def __init__(self, user_id, first_name, last_name, email, password_hash, phone, address, db: DatabaseManager):
        super().__init__(user_id, first_name, last_name, email, password_hash, phone, db)
        self._address = address
    
    #Determine if loading password into memory or hashed password is good (if its in the object)
    def view_dashboard(self):
        print(f"Welcome {self._first_name}")

        while True:
            match input(CUSTOMER_DASH):
                case "1":
                    self.book_taxi()
                case "2":
                    ...
                case "3":
                    self.cancel_booking
                case "4":
                    return
                case "5":
                    break
                case _:
                    print("Invalid Input. Please try again")
                

        
    
    

    def book_taxi(self):

        while True:
            pick_up = input("Please enter your desired pick up location: ")
            drop_off = input("Please enter your desired dropoff location: ")
            start_date = self._get_date()
            start_time = self._get_time()


            while True:
                print(dedent(f"""
                Please review your booking details:
                Pick Up Location: {pick_up}
                Drop-off Location: {drop_off}
                Date: {start_date}
                Time: {start_time}
                
                Please indicate your selection by choosing the appropriate number from the list below.
                1) Confirm
                2) Restart Booking Process
                3) Return to Menu

                Enter: 
                """))
                choice = input()
                match choice:
                    case "1":
                        start_datetime = datetime.combine(start_date, start_time)
                        self._db.create_booking(pick_up, drop_off, start_datetime, self)
                        return print("Booking was successfuly created!\n")

                        
                    case "2":
                        break
                    case "3":
                        return
                    case _:
                        print("Invalid Input. Please try again")
            
    def view_bookings(self):
        bookings = self._db.get_customer_bookings(self.user_id)
        ...
        current_booking = ... 
        #"""
        # All bookings whether or not completed will get passed into bookings, if boo
        # """
        
        ...

    def view_booking_history(self):
        bookings = self._db.get_customer_bookings(self.user_id)
        ...
        booking_history = ...
        ...
        test = tabulate[booking histoory, header]


    def cancel_booking(self, booking_id):
        ...

    """Private helper method to get and validate AM/PM datetime input"""
    def _get_date(self):
        while True:
            date = input("Please enter the booking date (DD/MM/YYYY).\nExample - '21/11/2026'.\nEnter: ")
            try:
                booking_date = datetime.strptime(date, "%d/%m/%Y").date()
                return booking_date
            except ValueError:
                print("Invalid date entered. Example - '21/11/2026' ")

            #FIX THIS AND MAKE IT SO THEY CANNOT BOOK BEFORE TODAY

    def _get_time(self):
        while True:
            time = input("Please enter the booking time (HH:MM AM/PM).\nExample - '2:30 AM'.\nEnter: ")
            try:
                booking_time = datetime.strptime(time, "%I:%M %p").time()
                return booking_time
            except ValueError:
                print("Invalid time entered. Example - '2:30 PM'")

            



class Driver(User):
    def __init__(self, user_id, first_name, last_name, email, password_hash, phone, db: DatabaseManager):
        super().__init__(user_id, first_name, last_name, email, password_hash, phone, db)


    def view_dashboard(self):
        print(f"Welcome {self._first_name}")
    
        while True:
            match input(DRIVER_DASH):
                case "1":
                    self.view_assigned_bookings()
                case "2":
                    ...
                case _:
                    print("Invalid Input. Please try again")

    def view_assigned_bookings(self):
        ...

class Administrator(User):
    def __init__(self, user_id, first_name, last_name, email, password_hash, phone):
        super().__init__(user_id, first_name, last_name, email, password_hash, phone)

    def view_dashboard(self):
        print(f"Welcome {self._first_name}")
    
        while True:
            match input(ADMINISTRATOR_DASH):
                case "1":
                    self.assign_driver()
                case "2":
                    ...
                case _:
                    print("Invalid Input. Please try again")


    def assign_driver(self, booking_id, driver_id):
        ...

    def view_all_bookings(self):
        ...


