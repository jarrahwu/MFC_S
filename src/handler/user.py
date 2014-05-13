#!/usr/bin/env python
#encoding=utf8
from bkmfc.uservice import exist_user
from bkmfc.validate import valid_pwd, valid_mobile
from bkmfc import codedef as DEFINE
from bkmfc.wrapper import BaseHandler
from bkmfc.uservice import register_user, get_id_user, update_user
def url_spec(*args, **kwargs):
    return [
        (r'/user/?', UserHandler, kwargs),
    ]

class UserHandler(BaseHandler):

    #get 获取用户信息
    def get(self, *args, **kwargs):
        token = self.get_token_cookie()
        if token:
            uid = token['uid']
            user_info = get_id_user(uid)
            self.write_back(code=1, **user_info)
            return

        else:
            self.write_back(**DEFINE.USER_NOT_FOUND)


    #修改用户信息
    def put(self, *args, **kwargs):
        token = self.get_token_cookie()
        uid = token['uid']

        #提供可以修改的字段
        u_keys = ['nick', 'gender', 'height', 'weight', 'age', 'bmi']
        params = self.get_body_json()
        if not params:
            self.write_back(**DEFINE.NO_MATCH_PARAMS)
            return

        modify_key_list = [modify_key for modify_key in u_keys if params.get(modify_key, False)]
        modify_value_list = []

        for key in modify_key_list:
            value = params.get(key, False)
            if value:
                modify_value_list.append(value)

        #把用户ID加进去
        modify_key_list.append('uid')
        modify_value_list.append(uid)

        #组合成dict
        user = {}
        for i in range(len(modify_key_list)):
            user.__setitem__(modify_key_list[i], modify_value_list[i])

        try:
            update_user(**user)
            user_info = get_id_user(user['uid'])
            if user_info:
                self.write_back(code=DEFINE.SUCCESS, **user_info)
                return
            else:
                self.write_back(**DEFINE.USER_UPDATE_FAIL)

        except:
            self.write_back(**DEFINE.USER_UPDATE_FAIL)
            return





    #post 注册用户信息
    def post(self, *args, **kwargs):
        """用户注册"""
        #检查是否有对应的参数
        user = {}
        user = self.check_params('mobile','password')

        if not user:
            self.write_back(**DEFINE.NO_MATCH_PARAMS)
            return

        #密码长度检验
        if not valid_pwd(user['password']):
            self.write_back(**DEFINE.PWD_LEN_NOT_VALID)
            return

        #用户账号检验,也就是电话号码的检验
        if not valid_mobile(user['mobile']):
            self.write_back(**DEFINE.USER_MOBILE_FORMAT_NOT_VALID)
            return

        #对密码进行前端加密和后台加密
       # user['password'] = hqlh.pwd.fore_sha1(params['password'])
       # user['password'] = hqlh.pwd.back_sha1(user['mobile'], user['password'])

        #用户有效性检验
        if not exist_user(**user):
            userId = register_user(**user)
            userInfo = get_id_user(userId)
            token = self.create_token(userId, userInfo['mobile'])
            userInfo['token'] = token
            self.write_back(status=200, code=1, **userInfo)
            return
        else:
            self.write_back(**DEFINE.USER_EXISTED)
            return

