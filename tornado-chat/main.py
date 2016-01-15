#!/usr/bin/env python

import basic_auth
import jot_handler
import json_parser
import myhost
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from base_app import CmdManager, BaseApplication
from userapp import UserApplicatin, MainHandler


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


def after_login(handler, user, pwd):
    handler.current_user = user
    handler.current_pwd = pwd


@basic_auth.basic_auth(check_credentials, after_login)
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
    def __init__(self, application, request, **kwargs):
        super(JsonHandler, self).__init__(application, request, **kwargs)
        self.dev_id = 0

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
        self.application.cmdManager.remove_handler(self)

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
        self.application.cmdManager.add_handler(self.dev_id, self)

        return True

    def test_timeout(self):
        print("test timeout")
        jstr = ' "req":"ST", "v":1, "req_id":"0x0001", "arg":{"tm":"2015-09-21T15:43:49.000+0000", "cmd":"0x01"}\r\n'
        self.write_message(jstr)

    def execute(self, message):
        self.write_message(message)


class DeviceApplication(BaseApplication):
    def __init__(self, _cmdmanager, **settings):
        super(DeviceApplication, self).__init__(_cmdmanager, **settings)
        handlers = [
            (r'/', MainHandler),
            (r'/sensors/v1/test-endpoint/?', JsonHandler),
            (r'/sensors/v1/([0-9,a-f,A-F,x]*)', SensorsHandler)
        ]
        tornado.web.Application.__init__(self, handlers, cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")


if __name__ == "__main__":
    cmdManager = CmdManager()

    devApp = DeviceApplication(cmdManager)
    http_server = tornado.httpserver.HTTPServer(devApp,
                                                ssl_options={
                                                    "certfile": os.path.join("certs/myserver.crt"),
                                                    "keyfile": os.path.join("certs/myserver.key"),
                                                })
    userApp = UserApplicatin(cmdManager)
    http_server80 = tornado.httpserver.HTTPServer(userApp)

    http_server.listen(8888)
    http_server80.listen(8080)

    tornado.ioloop.IOLoop.current().start()
