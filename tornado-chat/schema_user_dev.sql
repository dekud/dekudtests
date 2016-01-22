DROP TABLE IF EXISTS user_dev;
CREATE TABLE user_dev (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	sensor_id INT,
	user_id INT,
	INDEX (sensor_id),
	INDEX (user_id),
	FOREIGN KEY (sensor_id) REFERENCES sensors (id) ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);


