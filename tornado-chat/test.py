#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import MySQLdb
import torndb
import basic_auth
import jot_handler
import tornado.options

from tornado.options import define, options

define("mysql_host", default="127.0.0.1:3306", help="saggitarius database host")
define("mysql_database", default="saggitarius", help="saggitarius database name")
define("mysql_user", default="user", help="database user")
define("mysql_password", default="user", help="database password")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/',MainHandler),
			(r'/sensors/v1/test-endpoint/?',jot_handler.JoTHandler),
			(r'/sensors/v1/([^/]*)',SensorsHandler),
		]
		tornado.web.Application.__init__(self,handlers)
		
		self.db = torndb.Connection(
				host=options.mysql_host, database=options.mysql_database,
				user=options.mysql_user, password=options.mysql_password)
		for sensor in self.db.query("SELECT * from sensors"):
			print sensor


def check_credentials(handler, user, pwd):
	print user
	print pwd
	str = "SELECT * from sensors where device_id='"+user+"';"
	print(str)
	sensor = handler.application.db.query(str)
	print sensor
	if not sensor:
		return False
	if sensor[0].device_key == pwd:
		handler.token = sensor[0].token
		return True
	else:
		return False

def hello_fun(handler, kwargs, user, pwd):
	print(user)
	handler.current_user = user
	handler.current_pwd = pwd
	return

@basic_auth.basic_auth(check_credentials, hello_fun)
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		name = tornado.escape.xhtml_escape(self.current_user)
		self.write("Hello " + name )

@basic_auth.basic_auth(check_credentials, hello_fun)
class SensorsHandler(tornado.web.RequestHandler):
	def get(self, device_id):
		print(device_id)
		if device_id != self.current_user:
			raise tornado.web.HTTPError(404)

		self.redirect('/sensors/v1/test-endpoint?type=argus-controller&id='+device_id+'&token'+self.token)


if __name__ == "__main__":
	app = Application()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
