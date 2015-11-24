CREATE TABLE eventtypes (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	event_type INT NOT NULL,
	new TEXT,
	restore TEXT
);

CREATE TABLE devttypes (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	type_id INT NOT NULL,
	type_text TEXT,
	restore TEXT
);
