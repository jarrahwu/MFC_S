#!/usr/bin/env python
#coding: utf8

import hashlib

def fore_sha1(*args):
    """前台加密算法"""
    fore_pwd = hashlib.sha1(''.join(args)).hexdigest()
    return fore_pwd

def back_sha1(*args):
    """后台加密算法"""
    back_pwd = hashlib.sha1(''.join(args)).hexdigest()
    return back_pwd
