#!/usr/bin/env python
#coding:utf-8

import re

_EMAIL_PAT = re.compile(r'''
    ^([a-zA-Z0-9\-\_\.]+\@) # to match: abc123@
    ([a-zA-Z0-9\-]+\.)([a-zA-Z0-9\-]+\.{0,1}) # to match: qq.
    ([a-zA-Z0-9\-]*)$ # to match: com
    ''',re.VERBOSE)
#电话号码正则
_MOBILE_PAT = re.compile(r"^((13[0-9])|(14[0-9])|(17[0-9])|(15[0-9])|(18[0-9]))\d{8}$")

_PWD_MIN_LEN = 6
_PWD_MAX_LEN = 12

def valid_email(email):
    """检验邮箱格式
    """
    return True if _EMAIL_PAT.match(email) else False

def valid_mobile(mobile):
    """检查电话号码合法性
    """
    return True if _MOBILE_PAT.match(mobile) else False

def valid_pwd(pwd):
    """检验密码长度
    """
    return True if (_PWD_MIN_LEN <= len(pwd) <= _PWD_MAX_LEN) else False
