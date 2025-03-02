CREATE TABLE IF NOT EXISTS tokens (
    account_id INTEGER REFERENCES accounts(id),
    token VARCHAR(63)
)
