CREATE TABLE IF NOT EXISTS user_info (
    account_id INTEGER REFERENCES accounts(id),
    city VARCHAR(63),
    email VARCHAR(63),
    phone_number VARCHAR(15),
    last_login TIMESTAMP
)
