import sqlite3
import bcrypt
from pathlib import Path
from models import Customer, Driver, Administrator

ROLE_CLASSES = {
    "Customer" : Customer,
    "Driver": Driver,
    "Administrator" : Administrator
}


class DuplicateAccountError(Exception):
    """Email or phone is already registered."""

class BookingError(Exception):
    """Booking cannot be registered."""

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
        row = self._connection.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
        if row is None:
            return None

        if not bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
            return None

        return self._build_user(row)
        


    def _build_user(self, row):
        cls = ROLE_CLASSES[row["role"]]
        common = (row["user_id"], row["first_name"], row["last_name"], row["email"], row["password_hash"], row["phone"])

        if cls == Customer:
            return cls(*common, row["address"], self)
        return cls(*common, self)
        


    # Checks whether the specified email address is already registered in the database.
    def email_exists(self, email):
        row = self._connection.execute(
            "SELECT 1 FROM user WHERE email = ?", (email,)
        ).fetchone()
        return row is not None

    # Register a new customer in the database.
    def register_customer(self, first_name, last_name, email, password, phone, address):
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        sql = ("INSERT INTO user (first_name, last_name, email, password_hash, phone, address, role) VALUES (?, ?, ?, ?, ?, ?, 'Customer') RETURNING *")

        try:
            with self._connection:
                row = self._connection.execute(sql, (first_name, last_name, email, password_hash, phone, address)).fetchone()

        except sqlite3.IntegrityError as error:
            raise DuplicateAccountError("That email or phone number is already registered") from error

        return self._build_user(row)



    def create_booking(self, pick_up, drop_off, start_datetime, Customer: Customer):
                
        sql = ("INSERT INTO booking (pick_up, drop_off, start_datetime, customer_id) VALUES (?, ?, ?, ?)")

        try:
            with self._connection:
                self._connection.execute(sql, (pick_up, drop_off, start_datetime, Customer.user_id))

        except sqlite3.IntegrityError as error:
            raise BookingError("There was a problem creating this booking.") from error
        ...


    def get_customer_bookings(self, user_id):
        #SQL that pulls all bookings of the user based on the booking id, which will filter through customer id, and you do the thing like "row = self._connection", return row
        ...

    def update_booking(self, booking):
        ...


    def get_booking(self, booking_id):
        ...

    def get_unassigned_bookings(self):
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