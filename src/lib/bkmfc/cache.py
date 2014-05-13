# coding:utf-8

import redis
import tornadoredis

from hqlh.config import configs


_SYNC_CONNS_ = {}
_ASYNC_CONNS_ = {}
_IO_LOOP_ = None


def get_sync_conn(id):
    if id in _SYNC_CONNS_:
        return _SYNC_CONNS_[id]
    _SYNC_CONNS_[id] = conn = redis.Redis(**configs['redis'][id])
    return conn


def get_async_conn(id):
    if id in _ASYNC_CONNS_:
        return _ASYNC_CONNS_[id]
    _ASYNC_CONNS_[id] = conn = tornadoredis.Client(
        io_loop=_IO_LOOP_, **configs['redis'][id])
    conn.connect()
    return conn

