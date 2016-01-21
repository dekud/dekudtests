DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	login VARCHAR(128),
	password_hash VARCHAR(128),
	enabled INT,
	name VARCHAR(128),
	second_name VARCHAR(128),
	email TEXT
);


