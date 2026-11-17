from enum import Enum
from abc import ABC, abstractmethod

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
    def __init__(self, user_id, first_name, last_name, email, password_hash, phone):
        
        self._user_id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password_hash = password_hash
        self._phone = phone

    def verify_password(self, email, password):
        ...

    def logout(self):
        ...

    @abstractmethod
    def view_dashboard(self):
        ...



class Customer(User):
    def __init__(self, user_id, first_name, last_name, email, password_hash, phone, address):
        super().__init__(user_id, first_name, last_name, email, password_hash, phone)
        self._address = address

    def view_dashboard(self):
                ...
    
    

    def book_taxi(self, pick_up, drop_off, start_datetime):
        ...

    def cancel_booking(self, booking_id):
        ...


class Driver(User):
    def __init__(self, user_id, first_name, last_name, email, password_hash, phone):
        super().__init__(user_id, first_name, last_name, email, password_hash, phone)


    def view_dashboard(self):
        ...

    def view_assigned_bookings(self):
        ...

class Administrator(User):
    def __init__(self, user_id, first_name, last_name, email, password_hash, phone):
        super().__init__(user_id, first_name, last_name, email, password_hash, phone)

    def view_dashboard(self):
        ...

    def view_all_bookings(self):
        ...

    def assign_driver(self, booking_id, driver_id):
        ...