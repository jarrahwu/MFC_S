__author__ = 'jarrahwu'
#coding=utf8


import bkmfc.db
import handler.user
from bkmfc import codedef as CODE_DEF
import sys
import os
from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase, AsyncTestCase, AsyncHTTPClient
from bkmfc.config import configs
from tornado.web import Application, RequestHandler, create_signed_value
from tornado.escape import json_encode, json_decode
from bkmfc.wrapper import token_encode
class UserHandlerTestCase(AsyncHTTPTestCase):

    def setUp(self):
        AsyncHTTPTestCase.setUp(self)
        self.tt_token = {'uid': '1', 'mobile': '18682212241'}
        token = create_signed_value(
            configs['cookie_secret'], 'token',
            token_encode(self.tt_token)
        )
        self.tt_headers = {'Cookie': 'token=' + token}
        dbc = bkmfc.db.get_conn('bkmfc')
        dbc.execute('TRUNCATE user')

    def tearDown(self):
        dbc = bkmfc.db.get_conn('bkmfc')
        dbc.execute('TRUNCATE user')
        dbc = None
        pass

    def get_app(self):
        return Application(
            handler.user.url_spec(),
            cookie_secret=configs['cookie_secret']
        )

    def testRegister(self):

        self.normal_test()

        self.params_test()

        self.exist_test()

        self.user_modify_test()

        self.get_user_test()


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
        #已存在注册
        params = {"mobile":"18682212241","password":"18682212241"}
        response = self.fetch('/user', method='POST', body=json_encode(params))
        self.assertEqual(200,response.code)
        user_info = json_decode(response.body)
        self.assertEqual(CODE_DEF.USER_EXISTED['code'],user_info['code'])

    #测试user的put方法
    def user_modify_test(self): #运行这个测试之前,请确保要插入数据,因为前面一些test 已经把数据给清理掉了.
        #测试修改用户资料
        params = {"age":11, "nick":'lhkjkjfd', 'abcc':123}
        response = self.fetch('/user', method='PUT', headers=self.tt_headers,body=json_encode(params))
        self.assertEqual(200,response.code)
        user_info = json_decode(response.body)
        print(user_info)
        self.assertEqual(CODE_DEF.SUCCESS, user_info['code'])

        self.assertEqual(params["nick"], user_info['nick'])

    #测试 user的 get方法
    def get_user_test(self):
        response = self.fetch('/user', headers=self.tt_headers)
        user_info = json_decode(response.body)
        print("get user :", user_info)
        self.assertEqual(CODE_DEF.SUCCESS, user_info['code'])

