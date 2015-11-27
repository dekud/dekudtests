# -*- coding: utf-8 -*-
#!/usr/bin/env python

import MySQLdb
import torndb

#define("mysql_host", default="127.0.0.1:3306", help="saggitarius database host")
#define("mysql_database", default="saggitarius", help="saggitarius database name")
#define("mysql_user", default="user", help="database user")
#define("mysql_password", default="user", help="database password")


devtypes = [["РР","0x0000"],
["Маршрутизатор","0x0001"],
["Икар-Р","0x0100"],
["Икар-5Р","0x0101"],
["Аргус-Р","0x0102"],
["Икар-ШРШтора","0x0103"],
["Сокол-Р","0x0104"],
["Икар-Рисп.2","0x0105"],
["Аврора-Р","0x0200"],
["Аврора-ДТР","0x0201"],
["Аврора-ДР","0x0202"],
["Аврора-ТР","0x0203"],
["Амур-Р(ИПДЛ-Р)","0x0204"],
["Пламя-Р","0x0205"],
["Аврора-ДРисп.2","0x0206"],
["РИГ","0x0300"],
["Вода-Р(ДПВ-Р)","0x0301"],
["Градус-Р(ТД-Р)","0x0302"],
["Optex-Р","0x0303"],
["Газ-Р","0x0304"],
["УСЦП","0x0305"],
["РИГисп.2","0x0306"],
["РБУс4-мякнопками","0x0400"],
["Кнопка-Р(однакнопка)","0x0401"],
["СК-Р","0x0402"],
["Кнопка-Р","0x0403"],
["ИПР-Р","0x0500"],
["ИПР-РВ","0x0501"],
["ИБ-Ри.1","0x0600"],
["Арфа-Р","0x0700"],
["Арфа-2Р","0x0701"],
["ПультПУ-Р(о-п)","0x0800"],
["БПИRS-RF","0x0801"],
["ПультПУП-Р(пожарный)","0x0802"],
["ПУЛ-Р","0x0900"],
["ПУЛ0","0x0A00"],
["ШС1РРОП-2","0x0A01"],
["ШС2РРОП-2","0x0A02"],
["ВыходLMPРРОП-2","0x0A03"],
["ВыходSNDРРОП-2","0x0A04"],
["ИБ-Ри.2","0x0B00"],
["Сирена-Р","0x0B01"],
["Маячок(Wirelessbeacon)","0x0B02"],
["Сирена-Ри.2","0x0B03"],
["Аврора-ДСР","0x0B04"],
["ИБ-Ри.3","0x0B05"],
["УОО-АВисп.1","0x0C00"],
["УОО-Аргон","0x0C01"],
["УОО-GSM-C1","0x0C02"],
["УОО-Атлас-20","0x0C03"],
["УС-10С(Ethernet)","0x0C04"],
["ОСSM-RF","0x0C05"],
["Тандем-IP-И","0x0C06"],
["Орфей-Р","0x0D00"],
["Орфей-РТР","0x0D01"],
["Орфей-РУ","0x0D02"],
["Браслет-Р","0x0D03"],
["Табло-Р","0x0D04"],
["Аврора-ДОР","0x0D05"],
["Браслет-Р","0x0D06"],
["Аврора-ДОРисп.2","0x0D07"],
["БУК-Р","0x0E00"],
["ШС2БУК-Р","0x0E01"],
["ШС3БУК-Р","0x0E02"],
["ШС4БУК-Р","0x0E03"],
["РРП-240","0xF400"],
["РРОП","0xF500"],
["РРОП-И","0xF501"],
["РРОП-М","0xF502"],
["РРОП-2","0xF503"],
["РРОП-М2","0xF504"],
["ПКР-GSM","0xF505"],
["ПКРGSM2SIM","0xF506"],
["АСБ-РС","0xF600"]]


if __name__ == "__main__":
	db = torndb.Connection(host = "127.0.0.1:3306", database = "saggitarius", user = "user", password = "user")
	sensor = db.query("select * from sensors;")
	print sensor[0]
	nums = [i for i in range(127)]
	print nums
	for item in devtypes:
		strr = 'INSERT INTO devttypes (type_id, type_text) VALUES("'+str(int(item[1],0)) + '", "' + item[0]+'");'
		print strr
		db.execute(strr)