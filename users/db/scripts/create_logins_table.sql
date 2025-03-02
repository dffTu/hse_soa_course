CREATE TABLE IF NOT EXISTS logins (
    account_id INTEGER,
    login VARCHAR(63),
    hashed_password VARCHAR(63),
    is_freezed BOOLEAN,
    login_tries_in_1h INTEGER
)
