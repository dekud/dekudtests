# -*- coding: utf-8 -*-
#!/usr/bin/env python

import MySQLdb
import torndb

class dbcontroller:
	def __init__(self ,_host, _name, _user, _password):
		self.db = torndb.Connection(
				host=_host, database=_name,
				user=_user, password=_password)

	def getSensorByDevId(self, device_id):
		strq = "SELECT * from sensors where device_id='"+device_id+"';"
		print strq
		sensor = self.db.query(strq)
		if not sensor:
			return None
		return sensor[0]


	def pushConnectionEvent(self, device_id, ip_addr, text):
		[sensor_id, object_id] = self._getSensorAndObjIdByDevId(device_id)
		strq = "INSERT INTO connection_events (sensor_id, object_id, datetime, text, ip) VALUES(%s, %s, NOW(), %s, %s);"
		self.db.execute(strq,sensor_id, object_id, text, ip_addr)

	def pushEvent(self, device_id, json_dict):
		[sensor_id, object_id] = self._getSensorAndObjIdByDevId(device_id)
#		strq = ("INSERT INTO events (sensor_id, object_id, datetime, dev_datetime,text,"
#				"main_dev_category, main_dev_number,dev_category, dev_number, dev_type, t_object_category, t_objects) " 
#				"VALUES(%s, %s, NOW(), %s,"
#				"%s,%s, %s,"
#				"%s,%s, %s," 
#				"%s, %s);")
		
#		getEstr = "SELECT * from eventtypes where event_type="+json_dict.et+";"
#		eventtext = self.db.get(getEstr)
#		print eventtext
#		if json_dict.ef == "0x01":
#			text = eventtext.new
#		else:
#			text = eventtext.restore
		strq_t = ("INSERT INTO events (sensor_id, object_id, datetime, dev_datetime, event_type, event_flag, "
				"main_dev_category, main_dev_number,dev_category, dev_number, dev_type, t_object_category, t_objects) " 
				"VALUES('{0}','{1}', NOW(), '{2}',"
				"'{3}', '{4}', '{5}',"
				"'{6}', '{7}', '{8}'," 
				"'{9}', '{10}', '{11}');")
		strton = ""
		is_s = True
		for item in json_dict.ton:
			if is_s:
				strton = item
			else:
				strton = strton +", " + item

		strq = strq_t.format(sensor_id, object_id, json_dict.tm,
								int(json_dict.et, 0), int(json_dict.ef, 0), int(json_dict.dc1, 0),int( json_dict.dn1, 0),
								int(json_dict.dc2, 0), int(json_dict.dn2, 0), int(json_dict.dt2, 0),
								int(json_dict.toc, 0), strton) 

		print strq
#		self.db.execute(strq, sensor_id, device_id, json_dict.tm,
#								text, json_dict.dc1, json_dict.dn1,
#								json_dict.dc2, json_dict.dn2, json_dict.dt2,
#								json_dict.toc, json_dict.ton 
#								)
		self.db.execute(strq)

	def _getSensorAndObjIdByDevId(self, device_id):
		strq = "SELECT * from sensors where device_id='"+device_id+"';"
		sensor = self.db.get(strq)
		sensor_id = sensor.id
		object_id = sensor.object_id
		return [sensor_id, object_id]

