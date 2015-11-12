#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import basic_auth

class JoTHandler(tornado.web.RequestHandler):
	def __init__(self, application, request, **kwargs):
		tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
		self.stream = None

	@tornado.web.asynchronous
	def get(self):
		print("Argus-JoT")
		self.stream = self.request.connection.detach()
		self.stream.set_close_callback(self.on_connection_close)
		try:
			self.stream.write(tornado.escape.utf8(
				"HTTP/1.1 101 Switching Protocols\r\n"
				"Upgrade: argus-jot\r\n"
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

