# coding:utf8
'''
Created on 2013-8-29

@author: Administrator
'''
import json
import model.user

def register_user(**user):
    '''用户注册
    '''
    userInfo = model.user.create_user(user)
    return userInfo

def login_user(**user):
    '''用户登陆
    '''
    userInfo = model.user.login_user(user)
    return userInfo


def exist_user(**user):
    userInfo = model.user.exist_user(user)
    if userInfo:
        return userInfo
    else :
        return False


def get_id_user(uid):
    return model.user.id_user(uid)


def update_user(**user):
    model.user.update_user(user)