# coding:utf8

import bkmfc.db

def create_user(user):
    '''用户注册
    '''
    dbc = bkmfc.db.get_conn('bkmfc')
    sql = "INSERT INTO user (mobile,passwd) VALUES (%s,%s)"
    mobile = user['mobile']
    password = user['password']
    params = [mobile,password]
    userInfo = dbc.execute(sql, *params)
    return userInfo

def login_user(user):
    '''用户登陆
    '''
    dbc = bkmfc.db.get_conn('bkmfc')
    mobile = user['mobile']
    password = user['password']
    params = [mobile,password]
    userInfo = dbc.get("SELECT * FROM user WHERE mobile=%s and passwd=%s", *params)
    if userInfo :
        return userInfo
    else :
        return False

def exist_user(user):
    '''检查用户存在
    '''
    dbc = bkmfc.db.get_conn('bkmfc')
    mobile = user['mobile']
    params = [mobile]
    userInfo = dbc.get("SELECT * FROM user WHERE mobile=%s",*params)
    if userInfo:
        return userInfo
    else :
        return False

def id_user(uid):
    dbc = bkmfc.db.get_conn('bkmfc')
    userInfo = dbc.get("SELECT * FROM user WHERE id=%s",uid)

    if userInfo:return userInfo
    else :return False


def update_user(user):
    uid = user.get('uid', None)
    if not uid: return False

    sql_cmd = "UPDATE user SET "

    #把uid 去掉
    del(user['uid'])

    #获取需要update的字段
    key_set = user.keys()
    sql_clause = ''
    for key in key_set:
        sql_clause = ''.join([sql_clause, key, '=%s,'])#都加上逗号,多出来的一个最后去掉

    #去掉最后一个逗号 ','
    sql_clause = sql_clause[:-1]
    #添加 where 语句
    sql = sql_cmd + sql_clause + " WHERE id = %s" % uid

    params = user.values()
    dbc = bkmfc.db.get_conn('fitter')

    ret = dbc.execute(sql, *params)
    print ret,sql
    return ret

