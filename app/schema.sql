
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , username VARCHAR(66)
    , password VARCHAR(255) NOT NULL
);

CREATE table posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT
    , author_id INTEGER
    , title VARCHAR(66)
    , post TEXT
    , FOREIGN KEY (author_id) REFERENCES user(id) 
)