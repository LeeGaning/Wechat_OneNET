#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from logging.handlers import RotatingFileHandler

app = Flask(__name__, instance_relative_config=True)
#config.py
app.config.from_object('config')
# instance/config.py
app.config.from_pyfile('config.py')

# 记录日志
if not app.debug:
    import logging
    print(app.debug)
    logging.basicConfig()
    handler = RotatingFileHandler('log/app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)
    app.logger.info('--logging start--')

#路由设定
#import flask_web.routes
import flask_web.views.wechat

