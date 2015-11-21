SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";

CREATE TABLE IF NOT EXISTS  sensors (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(100) NOT NULL UNIQUE,
    device_id VARCHAR(100) NOT NULL UNIQUE,
    device_key VARCHAR(100) NOT NULL,
	object_id INT,
    updated TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS connection_events;
CREATE TABLE connection_events (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	sensor_id INT NOT NULL,
	object_id INT NOT NULL,
	datetime TIMESTAMP NOT NULL,
	text TEXT,
	ip VARCHAR(20)
);

DROP TABLE IF EXISTS objects;
CREATE TABLE objects (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name TEXT,
	phone TEXT,
	data BLOB
);

DROP TABLE IF EXISTS events;
CREATE TABLE events (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	sensor_id INT NOT NULL,
	object_id INT NOT NULL,
	datetime TIMESTAMP NOT NULL,
	dev_datetime VARCHAR(20),
	text TEXT,
	main_dev_category INT,
	main_dev_number INT,
	dev_category INT,
	dev_number INT,
	dev_type INT,
	t_object_category INT,
	t_objects TEXT,
	device_user INT,
	value_type INT,
	value INT
);
