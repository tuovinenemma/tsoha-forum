CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username UNIQUE TEXT,
    password TEXT
);

