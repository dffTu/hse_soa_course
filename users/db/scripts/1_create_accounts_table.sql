CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(63),
    surname VARCHAR(63),
    creation_date DATE,
    role VARCHAR(63)
)
