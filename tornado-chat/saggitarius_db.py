# -*- coding: utf-8 -*-
# !/usr/bin/env python

import torndb
import datetime


class dbcontroller:
    def __init__(self, _host, _name, _user, _password):
        self.db = torndb.Connection(
            host=_host, database=_name,
            user=_user, password=_password)

    def getSensorByDevId(self, device_id):
        strq = "SELECT * from sensors where device_id='" + device_id + "';"
        print strq
        sensor = self.db.query(strq)
        if not sensor:
            return None
        return sensor[0]

    def getLastEvents(self, id, device_id):
        qs ="SELECT * from sensors where sensors.device_id = '" + device_id + "';"
        dev = self.db.get(qs)
        if dev == None:
            return []

        strq = "SELECT * FROM events where id > " + id + " and sensor_id = "+ str(dev.id) + ";"

        events = self.db.query(strq)
        messages = []
        for ev in events:
            lt = ev.datetime + datetime.timedelta(hours=3)
            qs = "SELECT * from eventtypes where event_type = " + str(ev.event_type) + ";"
            etexts = self.db.get(qs)
            qs = "SELECT * from devttypes where type_id = " + str(ev.dev_type) + ";"
            devnames = self.db.get(qs)
            user_str = devnames.type_text + '[' + str(ev.dev_number) + ']'
            mm = {'user': user_str, 'text': ' '}
            if ev.event_flag == 1:
                mm['text'] = etexts.new
            else:
                mm['text'] = etexts.restore
            mm['datetime'] = str(lt)
            mm['id'] = str(ev.id)
            messages.append(mm)
        return messages

    def getEvents(self):
        strq = "SELECT * FROM events;"
        events = self.db.query(strq)
        messages = []
        for ev in reversed(events):
            lt = ev.datetime + datetime.timedelta(hours=3)
            qs = "SELECT * from eventtypes where event_type = " + str(ev.event_type) + ";"
            etexts = self.db.get(qs)
            qs = "SELECT * from devttypes where type_id = " + str(ev.dev_type) + ";"
            devnames = self.db.get(qs)
            user_str = devnames.type_text + '[' + str(ev.dev_number) + ']'
            mm = {'user': user_str, 'text': ' '}
            if ev.event_flag == 1:
                mm['text'] = etexts.new
            else:
                mm['text'] = etexts.restore
            mm['datetime'] = str(lt)
            messages.append(mm)
        return messages

    def pushConnectionEvent(self, device_id, ip_addr, text):
        [sensor_id, object_id] = self._getSensorAndObjIdByDevId(device_id)
        strq = "INSERT INTO connection_events (sensor_id, object_id, datetime, text, ip) VALUES(%s, %s, NOW(), %s, %s);"
        self.db.execute(strq, sensor_id, object_id, text, ip_addr)

    def pushEvent(self, device_id, json_dict):
        [sensor_id, object_id] = self._getSensorAndObjIdByDevId(device_id)
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
                strton = strton + ", " + item

        strq = strq_t.format(sensor_id, object_id, json_dict.tm,
                             int(json_dict.et, 0), int(json_dict.ef, 0), int(json_dict.dc1, 0), int(json_dict.dn1, 0),
                             int(json_dict.dc2, 0), int(json_dict.dn2, 0), int(json_dict.dt2, 0),
                             int(json_dict.toc, 0), strton)

        #print strq
        self.db.execute(strq)

    def getUserByName(self, login):
        qs = "SELECT * from users where login = '" + login + "';"
        user = self.db.get(qs)
        return user

    def saveUser(self, login, password, name, second_name, email):
        qs = "INSERT INTO users (login, password_hash, name, second_name, email, enabled) VALUES('"+login+"', '"+password+"', '"+name+"', '"+second_name+"', '"+email+"', 1);"
        print qs
        self.db.execute(qs)

    def getUserDevices(self, login):
        qs = "select u.login, d.device_id from users as u " \
             "left outer join user_dev as ud on u.id = ud.user_id " \
             "left outer join sensors as d on ud.sensor_id = d.id " \
             "where u.login = %s;"
        udev = self.db.get(qs,login)
        return udev

    def setUserDevice(self, login, dev_id):
        user = self.getUserByName(login)
        if user != None:
            qs = "insert into user_dev (user_id, sensor_id) VALUES ('%s', '%s');"
            self.db.execute(qs, user.id, dev_id)


    def addSensor(self, device_id, key, token):
        [sensor_id, object_id] = self._getSensorAndObjIdByDevId(device_id)
        if sensor_id == None:
            qs = "INSERT INTO sensors (device_id, device_key, token, object_id, updated ) VALUES (%s, %s, %s, '1', NOW());"
            self.db.execute(qs, device_id, key, token)
        [sensor_id, object_id] = self._getSensorAndObjIdByDevId(device_id)
        return sensor_id

    def _getSensorAndObjIdByDevId(self, device_id):
        strq = "SELECT * from sensors where device_id='" + device_id + "';"
        sensor = self.db.get(strq)
        if sensor == None:
            return [None, None]
        sensor_id = sensor.id
        object_id = sensor.object_id
        return [sensor_id, object_id]
