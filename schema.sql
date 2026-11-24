CREATE TABLE IF NOT EXISTS user (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  phone TEXT UNIQUE,
  address TEXT NULL,
  role TEXT NOT NULL CHECK (role IN ('Customer', 'Driver', 'Administrator'))

  
);

CREATE TABLE IF NOT EXISTS booking (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES user(user_id),
    driver_id INTEGER REFERENCES user(user_id),
    pick_up TEXT NOT NULL,
    drop_off TEXT NOT NULL,
    start_datetime TEXT NOT NULL,
    status TEXT NOT NULL
        DEFAULT 'Pending Driver Assignment'
        CHECK (
            status IN (
                'Pending Driver Assignment',
                'Driver Assigned',
                'Canceled'
            )
        )

);









