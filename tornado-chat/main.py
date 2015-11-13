#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import MySQLdb
import torndb
import basic_auth
import jot_handler
import tornado.options
import tornado.httpserver
import os

from tornado.options import define, options

import json_parser

define("mysql_host", default="127.0.0.1:3306", help="saggitarius database host")
define("mysql_database", default="saggitarius", help="saggitarius database name")
define("mysql_user", default="user", help="database user")
define("mysql_password", default="user", help="database password")


def check_credentials(handler, user, pwd):
	print user
	print pwd
	str = "SELECT * from sensors where device_id='"+user+"';"
	sensor = handler.application.db.query(str)
	if not sensor:
		return False
	if sensor[0].device_key == pwd:
		handler.token = sensor[0].token
		return True
	else:
		return False

def hello_fun(handler, kwargs, user, pwd):
	handler.current_user = user
	handler.current_pwd = pwd

@basic_auth.basic_auth(check_credentials, hello_fun)
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		name = tornado.escape.xhtml_escape(self.current_user)
		self.write("Hello " + name )

@basic_auth.basic_auth(check_credentials, hello_fun)
class SensorsHandler(tornado.web.RequestHandler):
	def get(self, device_id):
		if device_id != self.current_user:
			raise tornado.web.HTTPError(404)

		self.redirect('https://127.0.0.1/sensors/v1/test-endpoint?type=argus-controller&id='+device_id+'&token='+self.token )
	def on_finish(self):
		print "on close"

class JsonHandler(jot_handler.JoTHandler):
	def on_message(self, message):
		jparser = json_parser.JsonParser(message)
		print message
		self.write_message(jparser.get_result())

	def on_close(self):
		print('close')

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/',MainHandler),
			(r'/sensors/v1/test-endpoint/?',JsonHandler),
			(r'/sensors/v1/([^/]*)',SensorsHandler),
		]
		tornado.web.Application.__init__(self,handlers)
		
		self.db = torndb.Connection(
				host=options.mysql_host, database=options.mysql_database,
				user=options.mysql_user, password=options.mysql_password)
		for sensor in self.db.query("SELECT * from sensors"):
			print sensor

if __name__ == "__main__":
	app = Application()
	#app.listen(8888)
	http_server = tornado.httpserver.HTTPServer(app,
			ssl_options = {
			    "certfile": os.path.join("certs/myserver.crt"),
			    "keyfile": os.path.join("certs/myserver.key"),
			})
#	http_server.listen(8888)
#	tornado.ioloop.IOLoop.current().start()
	http_server.bind(8888)
	http_server.start(0)
	tornado.ioloop.IOLoop.current().start()

