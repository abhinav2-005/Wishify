CREATE DATABASE Whishify;

USE Whishify;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE wishes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipient_name VARCHAR(100) NOT NULL,
    wish_type VARCHAR(50) NOT NULL,
    wish_date DATE NOT NULL,
    recipient_email varchar(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


SELECT * FROM users;

SELECT * FROM wishes;

DROP TABLE 
users;

DROP TABLE
wishes;