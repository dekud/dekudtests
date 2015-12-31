#!/usr/bin/env python

import tornado.ioloop
import tornado.web
from tornado.iostream import StreamClosedError
import tornado.escape


class JoTHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        self.stream = None
        self.timeout = 0
        self._timer = tornado.ioloop.PeriodicCallback(self.connection_timeout, 10000)

    def on_message(self, message):
        """Implement this for recieve data"""
        raise NotImplementedError

    def write_message(self, message):
        """use this for wirite message to client"""
        message = tornado.escape.utf8(message)
        try:
            return self.stream.write(message)
        except StreamClosedError:
            self._abort()
        return

    def on_close(self):
        print("JoTHandler onClose")
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

            self._timer.start()
            self._receive_frame()

        except ValueError:
            print(ValueError.__dict__)
            self._abort()
            return
        except:
            print("Error")
            self._abort()
            return

    def _on_connection_close(self):
        self._timer.stop()
        self.on_close()
        pass

    def _receive_frame(self):
        try:
            self.stream.read_until(b"\r\n", self._on_read)
        except StreamClosedError:
            self._abort()

    def _on_read(self, data):
        print("_on_read")
        self.timeout = 0
        self.on_message(data)
        self._receive_frame()
        return

    def _abort(self):
        if not self.stream.closed():
            self.stream.close()
        self.on_close()

    def connection_timeout(self):
        self.timeout += 1
        if self.timeout == 12:
            self._abort()


