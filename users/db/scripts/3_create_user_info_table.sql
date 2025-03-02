CREATE TABLE IF NOT EXISTS user_info (
    account_id INTEGER REFERENCES accounts(id),
    city VARCHAR(63),
    email VARCHAR(63),
    phone_number VARCHAR(15),
    birthday DATE,
    last_login TIMESTAMP,
    last_update_info TIMESTAMP
)
