#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_web import app

# Start development web server
if __name__=='__main__':
    app.debug = app.config['DEBUG']
    app.run(host=app.config['HOST'],port=app.config['PORT'])