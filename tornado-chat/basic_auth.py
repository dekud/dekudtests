import base64

def basic_auth(auth_func=lambda *args, **kwargs: True, after_login_func=lambda *args, **kwargs: None, realm='Restricted'):
    def basic_auth_decorator(handler_class):
        def wrap_execute(handler_execute):
            def require_basic_auth(handler, kwargs):
                def create_auth_header():
                    handler.set_status(401)
                    handler.set_header('WWW-Authenticate', 'Basic realm=%s' % realm)
                    handler._transforms = []
                    handler.finish()

                auth_header = handler.request.headers.get('Authorization')

                if auth_header is None or not auth_header.startswith('Basic '):
                    create_auth_header()
                else:
                    auth_decoded = base64.decodestring(auth_header[6:])
                    user, pwd = auth_decoded.split(':', 2)

                    if auth_func(handler, user, pwd):
                        print "auth ok"
                        after_login_func(handler, user, pwd)
                    else:
                        create_auth_header()

            def _execute(self, transforms, *args, **kwargs):
                require_basic_auth(self, kwargs)
                return handler_execute(self, transforms, *args, **kwargs)

            return _execute

        handler_class._execute = wrap_execute(handler_class._execute)
        return handler_class
    return basic_auth_decorator
