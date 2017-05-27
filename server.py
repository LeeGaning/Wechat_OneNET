#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_web import app
if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.bind(app.config["PORT"], "127.0.0.1")
    http_server.start(0)
#http_server.listen(5000)
    IOLoop.instance().start()
