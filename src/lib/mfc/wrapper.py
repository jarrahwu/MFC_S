#/usr/bin/python
#coding=utf8
__author__ = 'jarrahwu'

import tornado.web
from tornado.escape import json_decode, json_encode
from tornado.web import decode_signed_value

#token编码
def token_encode(data):
        return '%s|%s' % (data['uid'], data['mobile'])
#token解码
def token_decode(data):
    ret = data.split('|')
    return {'uid': ret[0], 'mobile': ret[1]}

#cookie 过期时间
EXPIRES_DAY = 30


class BaseHandler(tornado.web.RequestHandler):

    def check_params(self, *keys):
        print self.request.body
        params = json_decode(self.request.body)
        params_got = {}
        for tmp_key in keys:
            params_got[tmp_key] = params.get(tmp_key, False)
            #如果找不到这个参数就返回参数不匹配
            if not params_got[tmp_key]:
                return False

        return params_got

    def write_back(self, status = 200, code = None, **info):
        # user_info = json_encode(info)
        if code:
            info['code'] = code

        self.write(info)
        self.set_status(status)

    #获取token
    def get_token_cookie(self, raise_error=True):
        """获取token。
            raise_error: 如果为真，没有token的时候抛出403异常，否则返回None
        """
        token = self.get_secure_cookie('token') #解码token tornado 自带
        if token:
            return token_decode(token)
        elif raise_error:
            raise tornado.web.HTTPError(403)
        else:
            return None


    #生成token
    def create_token(self, uid, mobile):
        return self.create_signed_value('token', '%s|%s' % (uid, mobile))

    #设置token
    def set_token_cookie(self, token):
        self.set_cookie("token", token, expires_days=EXPIRES_DAY)


    def get_body_json(self):
        try:
            params = json_decode(self.request.body)
        except:
            return None
        return params