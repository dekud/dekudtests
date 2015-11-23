# -*- coding: utf-8 -*-
#!/usr/bin/env python

import MySQLdb
import torndb

#define("mysql_host", default="127.0.0.1:3306", help="saggitarius database host")
#define("mysql_database", default="saggitarius", help="saggitarius database name")
#define("mysql_user", default="user", help="database user")
#define("mysql_password", default="user", help="database password")

event_text_lon = ["Постановка на охрану",																					       
	"Постановка на охрану с принуждением",
	"Сброс пожарных тревог и неисправностей",
	"Автоматическая постановка на охрану (перевзятие)",							       
	"Перевзятие на охрану ручное",			       
	"Сброс извещателя (адреса, ШС)",
	"",
	"",
	"Охранная тревога",																							       
	"Пожар 2",																							       
	"Паника",																												       
	"Задержка на снятие",																       
	"Пожар1",																						       
	"Пожарная тревога",												       
	"Технологическая тревога",																		       
	"Контроль прибытия наряда",	
	"Контроль прибытия наряда",
	"",
	"",		
	"",
	"",
	"",																       
	"",
	"Сигнал тревоги системы спасения пожарных Маяк спасателя",		
	"Неисправность устройства",	
	"Неисправность основного питания",																		       
	"Неисправность резервного питания",																			       
	"Отсутствие связи с устройством",																       
	"Запыление дымового извещателя",																       
	"Ручное исключение адреса",																					       
	"Автоматическое исключение адреса",																	       
	"Неисправность ШС",																							       
	"",
	"",
	"",
	"",	
	"",
	"",
	"",
	"",
	"Внешние радиоканальные помехи",																       
	"Разряд аккумулятора",
	"Неисправность аккумулятора",																		       
	"Отсутствие сетевого питания",																	       
	"Обобщённая неисправность",																			       
	"Обрыв основной линии связи с ПЦН",															       
	"Обрыв резервной линии связи с ПЦН",														       
	"Неисправность часов реального времени RTC",										       
	"Неисправность сигнальной линии",																       
	"Неисправность цепи контроля питания",													       
	"Ошибка конфигурирования устройства",
	"",
	"",
	"",	
	"",
	"",
	"Изменение кода доступа к устройству",													       
	"Программирование свойств устройства",													       
	"Добавление/изменение идентификационного признака пользователя",       
	"Программирование свойств извещателя/ШС",										           
	"Изменение чувствительности извещателя / порога ШС",				           
	"Перевод встроенных часов",
	"",												           
	"",
	"Включение устройства",																			           
	"Включение тестового режима",												
	"Включение извещателя",												
	"",												
	"",												
	"",												
	"",												
	"",												
	"Старт реле",	
	"",
	"Отключение группы ИУ",																			           
	"Старт оповещения",																					           
	"Команда на запуск аналоговой трансляции речевых сообщений",           
	"Запуск аналоговой трансляции речевых сообщений",						           
	"Команда “Стоп всех реле в группе ИУ”",
	"Пуск группы ИУ",
	"",							
	"",							
	"",							
	"",							
	"",							
	"",							
	"",							
	"",							
	"Вскрытие корпуса",																					           
	"Подбор кода доступа",																		           
	"Попытка подмены устройства",																           
	"Попытка несанкционированного управления выходом",					           
	"",
	"",
	"",
	"",
	"Начало отсчёта задержки пуска УПА",	  #96                               
	"Запуск УПА",         #97                                               
	"Старт тушения (выход огнетушащего вещества)",	  #98                     
	"Неудачный запуск УПА",	 #99                                     
	"Местный запуск УПА",	                                     
	"Блокировка запуска УПА",                                           
	"Отмена пуска УПА",	
	"Успешный запуск УПА",
	"Дистанционный запуск УПА",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"Предъявлен идентификатор пользователя",										           
	"Доступ предоставлен",                                
	"Проход пользователя в зону доступа",												           
	"Запрещение доступа в зону доступа",												           
	"Дверь слишком долго находится в открытом состоянии",		
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	""
]

event_rtext_lon = ["Снятие с охраны",
	"Снятие с охраны с принуждением",
	"Автоматический сброс пожарных тревог и неисправностей",
	"Автоматическое снятие с охраны",
	"–                             ",
	"–                             ",
	"",
	"",
	"Восстановление охранной тревоги",
	"Восстановление Пожара2",
	"Сброс паники",
	"Задержка на постановку",
	"Восстановление Пожара1",
	"–",
	"Восстановление технологической тревоги",
	"–",
	"" ,
	"" ,
	""	,	
	"" ,
	"" ,
	""	,															       
	"" ,
	""	,	
	"Норма устройства",
	"Норма основного питания",
	"Норма резервного питания",
	"Восстановление связи с устройством",
	"–                                           ",
	"Выключение ручного обхода",
	"Выключение автоматического обхода",
	"Норма ШС",																						       
	"",
	"",
	"",
	"",	
	"",
	"",
	"",
	"",
	"Прекращение воздействия радиоканальных помех",
	"Норма аккумулятора",
	"Норма аккумулятора",
	"Восстановление сетевого питания",
	"Восстановление обобщенная неисправность",
	"Восстановление основной линии связи с ПЦН",
	"Восстановление резервной линии связи с ПЦН",
	"Норма часов реального времени RTC",
	"Норма сигнальной линии",
	"Норма цепи контроля питания",													       
	"Норма конфигурации устройства",
	"",
	"",
	"",	
	"",
	"",
	"–",
	"–",
	"Удаление идентификационного признака пользователя",
	"Удаление извещателя/ШС", #59
	"", #60
	"", #61
	"",	#62											           
	"", #63
	"",	#64																		           
	"Выключение тестового режима",	#65											
	"Выключение извещателя",												
	"",												
	"",												
	"",												
	"",												
	"",												
	"Стоп реле",
	"",
	"Включение группы ИУ",
	"Стоп оповещения",
	"Команда на стоп аналоговой трансляции речевых сообщений",
	"Стоп аналоговой трансляции речевых сообщений",
	"Команда 'Старт всех реле в группе ИУ'",										           
	"Останов пуска ИУ" ,
	""	,						
	""	,						
	""	,						
	""	,						
	""	,						
	""	,						
	""	,						
	""	,						
	"Корпус закрыт" ,          
	""	,	           
	""	,		           
	""	,		           
	"" ,                
	"" ,              
	"" ,                
	"" ,                
	"Отмена запуска УПА" ,#96            
	"Отмена запуска УПА" ,#97             
	"" ,#98              
	"",	# 99 
	"", #100
	"Отмена блокировки запуска УПА", #101
	"", #102
	"Cтоп УПА", #103
	"", #104
	"", #105
	"", #106
	"", #107
	"", #108
	"", #109
	"", #110
	"", #111
	"", #112	           
	"Доступ отклонён" ,                 #113
	"Проход в зону совершён без предъявления идентификатора",
	"Разрешение доступа в зону доступа",
	"Восстановление нормального состояния двери",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	""
]

if __name__ == "__main__":
	db = torndb.Connection(host = "127.0.0.1:3306", database = "saggitarius", user = "user", password = "user")
	sensor = db.query("select * from sensors;")
	print sensor[0]
	nums = [i for i in range(127)]
	print nums
	for i in nums:
		strr = 'INSERT INTO eventtypes (event_type, new, restore) VALUES("'+str(i)+'", "' + event_text_lon[i] + '", "' + event_rtext_lon[i]+'");'
		print strr
		db.execute(strr)
		
		