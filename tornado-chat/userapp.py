import json
import json_parser
import tornado.web
from saggitarius_db import dbcontroller
from tornado.options import options
import tornado.escape
import base_app
import hashlib

class UserApplicatin(base_app.BaseApplication):
    def __init__(self, _cmdmanager, **settings):
        super(UserApplicatin, self).__init__(_cmdmanager, **settings)
        handlers = [
            (r'/', MainHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
            (r'/messages/?', MessageHandler),
            (r"/login", LoginHandler),
            (r"/create_user", CreateUserHandler),
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
            login = self.get_argument("name")
            password = self.get_argument("password")
            print login
            print password
            user = self.application.db_cont.getUserByName(login)
            m = hashlib.sha1()
            m.update(password)
            pass_hash = str(m.hexdigest())

            if user == None :
                print '000000'
                self.redirect("/login")
                return

            if (pass_hash != user.password_hash):
                self.redirect("/login")
                return

            print '11111'
        except tornado.web.MissingArgumentError:
            self.redirect("/login")
            return
        print '2222'
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

class CreateUserHandler(BaseHandler):
    def get(self):
        self.render('create_user.html')

    def post(self):
        try:
            login = self.get_argument("login")
            password = self.get_argument("password")
            name = self.get_argument("name")
            second_name = self.get_argument("second_name")
            email = self.get_argument("email")
            m = hashlib.sha1()
            m.update(password)
            pass_hash = m.hexdigest()
            print (login)
            print pass_hash
            user = self.application.db_cont.getUserByName(login)
            if user != None:
                self.redirect("/create_user")
                return

            self.application.db_cont.saveUser(login, pass_hash, name, second_name, email)

            self.redirect("/login")
        except tornado.web.MissingArgumentError:
            self.redirect("/create_user")
            return

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
        udev = self.application.db_cont.getUserDevices(name)
        print (udev)

        if udev != None:
            self.render('index.html', user=name, device=udev.device_id)
        else:
            self.render('index.html', user=name)

class MessageHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            _last = self.get_argument('last')
            device_id = self.get_argument('device')
        except tornado.web.MissingArgumentError:
            _last = 0
            device_id = 0
        messages = self.application.db_cont.getLastEvents(_last, device_id)
        self.write(json.dumps(messages))
        return
