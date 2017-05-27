#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,json
from flask_web import app

def red_led_on():
    headers = {'api-key': app.config["ONENET_TOKEN"]}
    payload = {'red_led': 1}
    r = requests.post(app.config["ONENET_URL"], headers=headers, data=json.dumps(payload))
    rc = json.loads(r.text).get("errno")
    if rc == 0:
        return "已点亮红灯！"
    else :
        return "操作失败!! 错误信息:"+json.loads(r.text).get("error")

def red_led_off():
    headers = {'api-key': app.config["ONENET_TOKEN"]}
    payload = {'red_led': 0}
    r = requests.post(app.config["ONENET_URL"], headers=headers, data=json.dumps(payload))
    rc = json.loads(r.text).get("errno")
    if rc == 0:
        return "已熄灭红灯！"
    else :
        return "操作失败!! 错误信息:"+json.loads(r.text).get("error")
