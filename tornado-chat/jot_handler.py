#!/usr/bin/env python

import tornado.ioloop
import tornado.web
from tornado.iostream import StreamClosedError


class JoTHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        self.stream = None

    def on_message(self, message):
        """Implement this for recieve data"""
        raise NotImplementedError

    def write_message(self, message):
        """use this for wirite message to client"""
        message = tornado.escape.utf8(message)
        try:
            return self.stream.write(message)
        except StreamClosedError:
            self.abort()
        return

    def on_close(self):
        pass

    def close(self):
        self._abort()

    def validate(self):
        return False

    @tornado.web.asynchronous
    def get(self):
        if not self.validate():
            raise tornado.web.HTTPError(400)
        print("Argus-JoT")
        self.stream = self.request.connection.detach()
        self.stream.set_close_callback(self._on_connection_close)
        try:
            self.stream.write(tornado.escape.utf8(
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: argus-jot\r\n"
                "Connection: Upgrade\r\n"
                "\r\n"))

            print("start receive 1")
            self._receive_frame()
            print("start receive 2")

        except ValueError:
            print(ValueError.__dict__)
            self._abort()
            return
        except:
            print("Error")
            self.abort()
            return

    def _on_connection_close(self):
        self.on_close()
        pass

    def _receive_frame(self):
        try:
            self.stream.read_until(b"\r\n", self._on_read)
        except StreamClosedError:
            self._abort()

    def _on_read(self, data):
        print("_on_read")
        self.on_message(data)
        self._receive_frame()
        return

    def _abort(self):
        if not self.stream.closed():
            self.stream.close()
        self.on_close()
