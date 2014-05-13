#usr/bin/python
#encoding=utf8
import sys
import os
from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase, AsyncTestCase, AsyncHTTPClient
from hqlh.config import configs
from tornado.web import Application, RequestHandler, create_signed_value
from tornado.escape import json_encode, json_decode

_TEST_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(_TEST_DIR, 'lib', 'poster-0.8.1-py2.6.egg'))
sys.path.append(os.path.join(_TEST_DIR, ''))

import hqlh.db
import handler.user
from hqlh import codedef as CODE_DEF
class RegisterHandlerTestCase(AsyncHTTPTestCase):

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        dbc = hqlh.db.get_conn('fitter')
        dbc.execute("TRUNCATE user")


    def tearDown(self):
        dbc = hqlh.db.get_conn('fitter')
        dbc.execute('TRUNCATE user')
        dbc = None

    def get_app(self):
        return Application(
            handler.user.url_spec(),
        )

    def testRegister(self):

        self.normal_test()

        self.params_test()

        self.exist_test()


    def normal_test(self):
        #正常注册
        params = {"mobile":"18682212241","password":"18682212241"}
        response = self.fetch('/user', method='POST', body=json_encode(params))
        self.assertEqual(200,response.code)
        user_info = json_decode(response.body)
        self.assertEqual(1,user_info['code'])

    def params_test(self):
        #参数不全
        params = {"mobile":"18682212241"}
        response = self.fetch('/user', method='POST', body=json_encode(params))
        self.assertEqual(200,response.code)
        user_info = json_decode(response.body)
        self.assertEqual(CODE_DEF.NO_MATCH_PARAMS['code'],user_info['code'])

    def exist_test(self):
        #正常注册
        params = {"mobile":"18682212241","password":"18682212241"}
        response = self.fetch('/user', method='POST', body=json_encode(params))
        self.assertEqual(200,response.code)
        user_info = json_decode(response.body)
        self.assertEqual(CODE_DEF.USER_EXISTED['code'],user_info['code'])