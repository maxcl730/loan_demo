# config.py
#import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

# debug = True
backlog = 2048
loglevel = 'debug'
bind = "0.0.0.0:7001"
pidfile = "logs/gunicorn.pid"
accesslog = "logs/access.log"
errorlog = "logs/debug.log"
daemon = True
# spew = True # debug

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'eventket'
x_forwarded_for_header = 'X-FORWARDED-FOR'