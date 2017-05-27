#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import date
from flask.views import View,MethodView
from flask import request, abort, jsonify, render_template, send_from_directory, make_response
from flask_web import app
from flask_web.plugins.led import red_led_on,red_led_off
class Index_view(MethodView):
    #methods = ['GET', 'POST']
    def get_template_name(self):
        raise NotImplementedError()
    def get(self):
        return render_template('index.html')
    def post(self):
        if request.is_json:
            data = request.json
            if data['red_led'] == 1:
                red_led_on()
            else :
                red_led_off()
            return make_response(jsonify({'Status': 'Successed'}), 200)
        return make_response(jsonify({'Status': 'Unauthorized Access'}), 403)

index_view = Index_view.as_view('index_view')
app.add_url_rule('/', view_func=index_view, methods=['GET', 'POST',])

class Static_view(MethodView):
    methods = ['GET']
    def get(self):
        return send_from_directory(app.static_folder, request.path[1:])

static_view = Static_view.as_view('static_view')
app.add_url_rule('/favicon.ico', view_func=static_view,methods=['GET'])
app.add_url_rule('/robots.txt', view_func=static_view,methods=['GET'])

