#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import basic_auth
import jot_handler
import tornado.options
import tornado.httpserver
import os
from saggitarius_db import dbcontroller
from six import print_
from tornado import ioloop
from tornado.options import define, options
import json_parser
import json
import myhost

define("mysql_host", default="127.0.0.1:3306", help="saggitarius database host")
define("mysql_database", default="saggitarius", help="saggitarius database name")
define("mysql_user", default="user", help="database user")
define("mysql_password", default="user", help="database password")


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        try:
            if self.get_argument("password") != "streletz":
                self.redirect("/login")
                return
        except tornado.web.MissingArgumentError:
            self.redirect("/login")
            return

        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")


class CmdHandler(BaseHandler):
    def get(self):
        try:
            cmd = self.get_argument("cmd")
            dev = self.get_argument("dev")
            jc = json_parser.JsonCmd(cmd)
            print(jc.get_json())
            self.application.jhandlers[dev].sendcmd(jc.get_json())
        except tornado.web.MissingArgumentError:
            print ("cmd err")
        except KeyError:
            print self.application.jhandlers


def check_credentials(handler, user, pwd):
    print("device_id: " + user)
    print("device_key: " + pwd)
    sensor = handler.application.db_cont.getSensorByDevId(user)
    if not sensor:
        return False
    if sensor.device_key == pwd:
        handler.token = sensor.token
        return True
    else:
        return False


def hello_fun(handler, kwargs, user, pwd):
    handler.current_user = user
    handler.current_pwd = pwd


# @basic_auth.basic_auth(check_credentials, hello_fun)
class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        if name != "cloud":
            self.redirect("/login")
            return
        messages = self.application.db_cont.getEvents()
        self.render('index.html', messages=messages, user=name, device='0x00000000010203AB')


class MessageHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            _last = self.get_argument('last')
        except tornado.web.MissingArgumentError:
            _last = 0
        messages = self.application.db_cont.getLastEvents(_last)
        self.write(json.dumps(messages))


@basic_auth.basic_auth(check_credentials, hello_fun)
class SensorsHandler(tornado.web.RequestHandler):
    def get(self, device_id):
        if device_id != self.current_user:
            raise tornado.web.HTTPError(404)
        h = myhost.myhost()
        self.redirect(
            'https://' + h.host + '/sensors/v1/test-endpoint?type=argus-controller&id=' + device_id + '&token=' + self.token)

    def on_finish(self):
        print "SensorsHandler on close"


class JsonHandler(jot_handler.JoTHandler):
    @property
    def db_cont(self):
        return self.application.db_cont

    def on_message(self, message):
        jparser = json_parser.JsonParser(message)
        answer = jparser.get_result()
        if jparser.isEventToDB:
            self.db_cont.pushEvent(self.dev_id, jparser.events[0])

        if answer['has_answer']:
            print("json answer: " + answer['txt'])
            self.write_message(answer['txt'])

    def on_close(self):
        self.db_cont.pushConnectionEvent(self.dev_id, self.request.remote_ip, 'Close connection')
        print('JsonHandler close')
        if self.application.jhandlers[self.dev_id] == self:
            del self.application.jhandlers[self.dev_id]

    def validate(self):
        print "JsonHandler validate:"
        try:
            self.dev_id = self.get_argument('id')
            _type = self.get_argument('type')
            _token = self.get_argument('token')
            print self.dev_id
            sensor = self.db_cont.getSensorByDevId(self.dev_id)
        except:
            return False

        if not sensor:
            return False
        if _type != 'argus-controller' or _token != sensor.token:
            return False

        self.db_cont.pushConnectionEvent(self.dev_id, self.request.remote_ip, 'Open connection')
        self._timer = tornado.ioloop.PeriodicCallback(self.test_timeout, 40000)
        # self._timer.start()

        self.application.jhandlers[self.dev_id] = self

        return True

    def test_timeout(self):
        print("test timeout")
        jstr = ' "req":"ST", "v":1, "req_id":"0x0001", "arg":{"tm":"2015-09-21T15:43:49.000+0000", "cmd":"0x01"}\r\n'
        self.write_message(jstr)

    def sendcmd(self, j):
        self.write_message(j)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/sensors/v1/test-endpoint/?', JsonHandler),
            (r'/sensors/v1/([0-9,a-f,A-F,x]*)', SensorsHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
            (r'/messages/?', MessageHandler),
            (r"/login", LoginHandler),
            (r"/logout", AuthLogoutHandler),
            (r"/cmd/?", CmdHandler),

        ]
        tornado.web.Application.__init__(self, handlers, cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")

        self.db_cont = dbcontroller(
            options.mysql_host, options.mysql_database,
            options.mysql_user, options.mysql_password)

        self.jhandlers = {}


if __name__ == "__main__":
    app = Application()
    # app.listen(8888)
    http_server = tornado.httpserver.HTTPServer(app,
                                                ssl_options={
                                                    "certfile": os.path.join("certs/myserver.crt"),
                                                    "keyfile": os.path.join("certs/myserver.key"),
                                                })
    # http_server.listen(8888)
    # tornado.ioloop.IOLoop.current().start()
    http_server.bind(8888)
    http_server.start(0)
    tornado.ioloop.IOLoop.current().start()
