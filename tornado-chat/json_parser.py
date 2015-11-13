#!/usr/bin/env python

import json

class JDeivce:
	def __init__(self, dic):
		pass		

class JReqArg:
	def __init__(self,dic):
		print dic
		self.__dict__ = dic
		print dic

class JReq:
	req = ''
	v = 0
	req_id = ''
	arg = None
	def __init__(self, dic):
		self.__dict__ = dic
		print dic
		if u'arg' in dic:
			self.arg = JReqArg(dic[u'arg'])


class JReqAnswer:
	req_answer = ''
	v = 0
	req_id = ''
	err_code = '0xff'
	arg = None
	def __init__(self, dic):
		self.__dict__ = dic
		print dic
		if u'arg' in dic:
			self.arg = JReqArg(dic[u'arg'])

class JsonParser:
	def __init__(self, message):
		try:
			dic = json.loads(message)
			print dic
			if u'req' in dic:
				req = JReq(dic)
				self.txt = self._on_req(req)
			elif u'req_answ' in dic:
				req_answ = JReqAnswer(dic)
				self.txt = 'this is req_answ'
			elif u'device_id' in dic:
				self.txt  = 'this is configuration'
		except:
			self.txt = 'error json'
			raise 
			pass
	
	def get_result(self):
		return self.txt + ' ok\r\n'
	
	def _on_req(self, req):
		if req.req == u'PING':
			dic = {'req_answ' : req.req, 'v' : req.v, 'req_id': req.req_id ,'err_code' : '0x00'}
			return json.dumps(dic)
		else:
			dic = {'req_answ' : req.req, 'v' : req.v, 'req_id': req.req_id ,'err_code' : '0x00'}
			return json.dumps(dic)
	
	def _on_req_answer(self, req_answ):
		pass

	
