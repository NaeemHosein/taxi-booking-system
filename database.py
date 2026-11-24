import sqlite3
import bcrypt
from pathlib import Path
from models import Customer, Driver, Administrator

class DuplicateAccountError(Exception):
    """Email or phone is already registered"""


class DatabaseManager:
    def __init__(self, db_name="taxi_booking.db"):
        self._connection = sqlite3.connect(db_name)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")

        schema = Path(__file__).with_name("schema.sql")
        self._connection.executescript(schema.read_text("utf-8"))

        with open("schema.sql") as f:
            self._connection.executescript(f.read())

    def authenticate(self, email, password):
        #This is suppose to look into the database to see if the email and password matches, make sure and use the password hashing to see this.
        #If this matches then you call on _build_user with the row to build out the user object depending on what user it is.
        ...
        


    def _build_user(self, row):
        #build out user, (taking in the row, this is suppose to determine if the user role is a customer, driver, admin then create the object based on it.)
        ...


    # Checks whether the specified email address is already registered in the database.
    def email_exists(self, email):
        row = self._connection.execute(
            "SELECT 1 FROM user WHERE email = ?", (email,)
        ).fetchone()
        return row is not None

    # Register a new customer in the database.
    def register_customer(self, first_name, last_name, email, password, phone, address):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        sql = ("INSERT INTO user (first_name, last_name, email, password_hash, phone, address, role) VALUES (?, ?, ?, ?, ?, ?, 'Customer')")

        try:
            with self._connection:
                self._connection.execute(sql, (first_name, last_name, email, password_hash, phone, address))

        except sqlite3.IntegrityError as error:
            raise DuplicateAccountError("That email or phone number is already registered") from error
        


    def create_booking(self, pick_up, drop_off, start_datetime, Customer):
        # Priority 1 - Mehlik - Make the code here to insert the booking information into the database.
        # Take inspiration from register customer
        # Suppose to store the user_id from customer in the customer_id column in the booking information.
        # use the with self._connection to have the cursor
        ...

    def update_booking(self, booking):
        ...

    def get_booking(self, booking_id):
        ...

    def get_all_bookings(self):
        ...


    def is_driver_available(self, driver, start_datetime):
        ...

    def get_driver_bookings(self, driver):
        ...

    def get_drivers(self):
        ...

    def close(self):
        self._connection.close()