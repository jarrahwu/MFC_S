#!/usr/bin/env python
# coding: utf-8

import os
import sys
import unittest


TEST_MODULES = [
     'auth_test',
     'user_test',
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)


if __name__ == '__main__':
    # src_path = os.path.abspath(os.path.join(
    #             os.path.dirname(__file__), '/'))
    src_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '..', 'src'))
    print src_path
    if src_path not in sys.path:
        # 调整包含路径
        sys.path.append(src_path)
        sys.path.append(os.path.join(src_path, 'bin'))
        sys.path.append(os.path.join(src_path, 'lib'))
        sys.path.append(os.path.join(src_path, 'lib', 'poster-0.8.1-py2.6.egg'))
    from bkmfc.config import configs, load_conf_file
    load_conf_file(os.path.join(src_path, 'etc', 'db.conf'))
    load_conf_file(os.path.join(src_path, 'etc', 'mfc.conf'))
    import tornado.testing
    tornado.testing.main()

