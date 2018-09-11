CREATE TABLE genre
(
    id integer PRIMARY KEY,
    name text NOT NULL
);
CREATE TABLE game
(
    id integer PRIMARY KEY,
    name text NOT NULL,
    genre_id integer NOT NULL,
    link text,
    up integer,
    down integer,
    FOREIGN KEY(genre_id) references genres(id)
);
CREATE TABLE user
(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    admin BOOLEAN NOT NULL DEFAULT 0,
    password TEXT,
    deleted BOOLEAN NOT NULL DEFAULT 1
);
CREATE TABLE comment
(
    id INTEGER PRIMARY KEY,
    gameid INTEGER NOT NULL,
    userid INTEGER NOT NULL,
    comment TEXT,
    promoted BOOLEAN NOT NULL DEFAULT 0,
    up INTEGER,
    down INTEGER,
    date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
