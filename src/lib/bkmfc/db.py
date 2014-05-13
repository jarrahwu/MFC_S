# coding: utf-8
""" Database工具。
"""

import redis
import tornadoredis
from torndb import Connection

from bkmfc.config import configs


_SYNC_REDIS_ = {}
_ASYNC_REDIS_ = {}


def get_sync_redis(id):
    if id in _SYNC_REDIS_:
        return _SYNC_REDIS_[id]
    _SYNC_REDIS_[id] = conn = redis.StrictRedis(**configs['redis'][id])
    return conn


def get_async_redis(id, exclusive=False, io_loop=None):
    params = configs['redis'][id].copy()
    params['selected_db'] = params.pop('db', 0)
    if exclusive:
        conn = tornadoredis.Client(io_loop=io_loop, **params)
        conn.connect()
        return conn
    if id in _ASYNC_REDIS_:
        return _ASYNC_REDIS_[id]
    _ASYNC_REDIS_[id] = conn = tornadoredis.Client(
        io_loop=io_loop, **params)
    conn.connect()
    return conn


############################################################


_SYNC_MYSQL_ = {}


def get_sync_mysql(db_id):
    if db_id in _SYNC_MYSQL_:
        return _SYNC_MYSQL_[db_id]
    _SYNC_MYSQL_[db_id] = db = Connection(**configs['mysql'][db_id])
    db._db_args.pop('init_command', None)
    db.execute("SET TIME_ZONE = 'SYSTEM'")
    return db

get_conn = get_sync_mysql

