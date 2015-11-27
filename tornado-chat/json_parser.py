#!/usr/bin/env python

import json


class JDeivce:
    def __init__(self, dic):
        pass


class JReqArg:
    def __init__(self, dic):
        print("arg: ")
        print(dic)
        self.__dict__ = dic


class JReqEvent:
    def __init__(self, dic):
        print "event: "
        print dic
        self.__dict__ = dic


class JReqEventArg:
    def __init__(self, dic):
        self.events = []
        self.events = [JReqEvent(i) for i in dic[u'e']]
        print self.events[0]


class JReq:
    req = ''
    v = 0
    req_id = ''
    arg = None

    def __init__(self, dic):
        self.__dict__ = dic
        print("req: ")
        print(dic)
        if u'arg' in dic:
            if self.req == u'EVENT':
                self.arg = JReqEventArg(dic[u'arg'])
            else:
                self.arg = JReqArg(dic[u'arg'])


class JReqAnswer:
    req_answer = ''
    v = 0
    req_id = ''
    err_code = '0xff'
    arg = None

    def __init__(self, dic):
        self.__dict__ = dic
        print("req answ: ")
        print(dic)
        if u'arg' in dic:
            self.arg = JReqArg(dic[u'arg'])


class JsonParser:
    def __init__(self, message):
        self.isEventToDB = False
        self.events = []
        try:
            print("JSON str: " + message)
            dic = json.loads(message)
            if u'req' in dic:
                req = JReq(dic)
                self.txt = self._on_req(req)
            elif u'req_answ' in dic:
                req_answ = JReqAnswer(dic)
                self.txt = 'this is req_answ'
            elif u'device_id' in dic:
                self.txt = 'this is configuration'
        except:
            self.txt = 'error json'
            raise
            pass

    def get_result(self):
        return self.txt + ' ok\r\n'

    def _on_req(self, req):
        if req.req == u'PING':
            dic = {'req_answ': req.req, 'v': req.v, 'req_id': req.req_id, 'err_code': '0x00'}
            return json.dumps(dic)
        elif req.req == u'EVENT':
            print req.arg.events[0].ef
            self.events = req.arg.events
            self.isEventToDB = True
            dic = {'req_answ': req.req, 'v': req.v, 'req_id': req.req_id, 'err_code': '0x00'}
            return json.dumps(dic)
        else:
            dic = {'req_answ': req.req, 'v': req.v, 'req_id': req.req_id, 'err_code': '0x00'}
            return json.dumps(dic)

    def _on_req_answer(self, req_answ):
        pass
