#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import basic_auth

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/',MainHandler),
			(r'/test',TestHandler),
			(r'/sensors/v1/([^/]*)',SensorsHandler),
		]
		tornado.web.Application.__init__(self,handlers)



def check_credentials(user, pwd):
	return True #user == 'foo'

def hello_fun(handler, kwargs, user, pwd):
	print(user)
	handler.current_user = user
	return

@basic_auth.basic_auth(check_credentials, hello_fun)
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		name = tornado.escape.xhtml_escape(self.current_user)
		self.write("Hello " + name )

@basic_auth.basic_auth(check_credentials, hello_fun)
class SensorsHandler(tornado.web.RequestHandler):
	def get(self, t):
		print(t)
		name = tornado.escape.xhtml_escape(self.current_user)
		#self.write("Hello " + name )
		self.redirect('/test')

class TestHandler(tornado.web.RequestHandler):
	def __init__(self, application, request, **kwargs):
		tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
		self.stream = None

	@tornado.web.asynchronous
	def get(self):
		print("La-La-La")
		self.stream = self.request.connection.detach()
		print("---1---")
		self.stream.set_close_callback(self.on_connection_close)
		print("---2---")
		try:
			self.stream.write(tornado.escape.utf8(
				"HTTP/1.1 101 Switching Protocols\r\n"
				"Upgrade: test\r\n"
				"Connection: Upgrade\r\n"
			"\r\n"))
			
			self._receive_frame()

		except ValueError:
			print(ValueError.__dict__)
			self._abort()
		except:
			print("Error")

		print("---3---")
	
	def on_connection_close(self):
		print("close")
		pass
	
	def _receive_frame(self):
		try:
			self.stream.read_bytes(2, self._on_frame_start)
		except StreamClosedError:
			self._abort()

	def _on_frame_start(self,data):
		print(data)
		self.stream.write(tornado.escape.utf8("""{"req": "PING", "v": 1, "req_id": "0x0666", "arg": {}}"""))
		self.stream.read_bytes(10,self._on_frame_start)
		pass

	def _abort(self):
		self.stream.close()

def make_app():
	return tornado.web.Application([ (r"/", MainHandler), ])

if __name__ == "__main__":
	app = Application()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()
