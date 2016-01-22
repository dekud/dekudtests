insert into user_dev (user_id, sensor_id)
	select users.id, sensors.id from users, sensors
	where users.login = user or sensors.device_id = 0x00000000010203AB;

