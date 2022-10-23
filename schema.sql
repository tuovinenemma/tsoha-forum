CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
    role integer
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    headline TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    message_id INTEGER REFERENCES messages,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    liked INTEGER,
    user_id INTEGER REFERENCES users,
    message_id INTEGER REFERENCES messages
);

CREATE TABLE dislikes (
    id SERIAL PRIMARY KEY,
    disliked INTEGER,
    user_id INTEGER REFERENCES users,
    message_id INTEGER REFERENCES messages
);