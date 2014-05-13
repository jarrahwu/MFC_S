#coding=utf8
'''定义一些返回的code
'''
PWD_LEN_NOT_VALID = {'code':10001,'msg':"密码长度不符合"}

USER_EXISTED = {'code':10002, 'msg':'用户已经存在'}

USER_MOBILE_FORMAT_NOT_VALID = {'code':10003, 'msg':'用户账号不是电话格式'}

NO_MATCH_PARAMS = {'code':10004, 'msg':'没有对应的参数'}

USER_NOT_FOUND = {'code':10005, 'msg':'用户密码或者账号错误'}

USER_UPDATE_FAIL = {'code':10007, 'msg':'更新用户资料失败'}

SUCCESS = 1