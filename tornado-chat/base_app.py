import tornado.web
from saggitarius_db import dbcontroller
from tornado.options import options
from tornado.options import define

define("mysql_host", default="127.0.0.1:3306", help="saggitarius database host")
define("mysql_database", default="saggitarius", help="saggitarius database name")
define("mysql_user", default="user", help="database user")
define("mysql_password", default="user", help="database password")


class CmdManager:
    def __init__(self):
        self.handlers = []

    def add_handler(self, dev_id, handler):
        handler_dict = dict(id=dev_id, handler=handler)
        self.handlers.append(handler_dict)

    def remove_handler(self, handler):
        for hdict in self.handlers:
            if hdict['handler'] == handler:
                self.handlers.remove(hdict)
                break

    def execute_handler(self, dev_id, params):
        for hdict in self.handlers:
            if hdict['id'] == dev_id:
                hdict['handler'].execute(params)


class BaseApplication(tornado.web.Application):
    def __init__(self, _cmdmanager, **settings):
        """
        :type _cmdmanager: CmdManager
        :param _cmdmanager:CmdManager
        :return:
        """
        super(BaseApplication, self).__init__(**settings)
        self.db_cont = dbcontroller(
            options.mysql_host, options.mysql_database,
            options.mysql_user, options.mysql_password)

        assert isinstance(_cmdmanager, CmdManager)
        self.cmdManager = _cmdmanager
