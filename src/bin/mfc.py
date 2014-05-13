#!/usr/bin/env python
#coding=utf8

import os.path
import sys

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if src_path not in sys.path:
    lib_path = os.path.join(src_path, 'lib')
    sys.path.append(src_path)
    sys.path.append(lib_path)

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from bkmfc.config import configs, load_conf_file

class Application(tornado.web.Application):
    def __init__(self):
        #db = hqby.db.get_conn('fitter_sport')
        handlers = []
        handler_mods = [
            'auth',
            'user',
        ]
        for i in handler_mods:
            m = __import__('handler.' + i, fromlist=['url_spec'])
            handlers.extend(m.url_spec())

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            cookie_secret=configs['cookie_secret'],
            autoescape=None,
            debug=configs['debug'],
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(configs['port'])
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    load_conf_file(os.path.join(src_path, 'etc', 'db.conf'))
    load_conf_file(os.path.join(src_path, 'etc', 'mfc.conf'))
    main()
