#usr/bin/python
#encoding=utf8
import sys
import os
from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase, AsyncTestCase, AsyncHTTPClient
from bkmfc.config import configs
from tornado.web import Application, RequestHandler, create_signed_value
from tornado.escape import json_encode, json_decode

_TEST_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(_TEST_DIR, 'lib', 'poster-0.8.1-py2.6.egg'))
sys.path.append(os.path.join(_TEST_DIR, ''))

import bkmfc.db
import handler.auth

class LoginHandlerTestCase(AsyncHTTPTestCase):

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        dbc = bkmfc.db.get_conn('bkmfc')
        dbc.execute("TRUNCATE user")


    def tearDown(self):
        dbc = bkmfc.db.get_conn('bkmfc')
        dbc.execute('TRUNCATE user')
        dbc = None

    def get_app(self):
        return Application(
            handler.auth.url_spec(),

        )

    def testLogin(self):
        #正确登录
        params = {"mobile":"18682212241","password":"18682212241"}
        response = self.fetch('/user/login', method='POST', body=json_encode(params))
        self.assertEqual(200,response.code)

        #密码错误test
        params["password"] = "18682272271"
        response = self.fetch('/user/login', method="POST", body=json_encode(params))
        info = json_decode(response.body)
        self.assertEqual(10005,info['code'])

        #参数不全test
        params["mobile"] = "18682272271"
        del params["password"]
        response = self.fetch('/user/login', method="POST", body=json_encode(params))
        info = json_decode(response.body)
        self.assertEqual(10004,info['code'])

