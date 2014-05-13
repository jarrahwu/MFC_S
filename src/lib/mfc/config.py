# coding: utf-8
"""配置模块，负责加载配置，并供其它模块使用。
"""

import os

from tornado import options


configs = {}

def load_conf_file(path=None):
    """加载配置文件
    """
    if path and os.path.isfile(path):
        execfile(path, {}, configs)
    # 命令行输入的参数具有最高优先级，每次加载完配置文件都重新覆盖一次
    if options.options['conf']:
        execfile(options.options['conf'], {}, configs)
    if options.options['port']:
        configs['port'] = options.options['port']


options.define('port', default=0, help='server listening port', type=int)
options.define('conf', default=None, help='configuration file', type=str)
options.parse_command_line()
load_conf_file()

