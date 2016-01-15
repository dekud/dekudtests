import json

import json_parser
import tornado.web
from saggitarius_db import dbcontroller
from tornado.options import options
import tornado.escape
import base_app


class UserApplicatin(base_app.BaseApplication):
    def __init__(self, _cmdmanager, **settings):
        super(UserApplicatin, self).__init__(_cmdmanager, **settings)
        handlers = [
            (r'/', MainHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
            (r'/messages/?', MessageHandler),
            (r"/login", LoginHandler),
            (r"/logout", AuthLogoutHandler),
            (r"/cmd/?", CmdHandler),

        ]
        tornado.web.Application.__init__(self, handlers, cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")
        print(self.cmdManager)

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
            self.application.cmdManager.execute_handler(dev, jc.get_json())
        except tornado.web.MissingArgumentError:
            print ("cmd err")
        except KeyError:
            print self.application.jhandlers


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
