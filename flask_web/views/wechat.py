#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests,json
import time
from flask.views import MethodView
from flask import request, abort
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
	InvalidSignatureException,
	InvalidAppIdException,
)
from flask_web import app

def wechat_response(msg):
	"""微信消息处理回复"""
	global message
	message = msg
	try:
		get_resp_func = msg_type_resp[message.type]
		response = get_resp_func()
	except KeyError:
		# 默认回复微信消息
		response = 'Sorry, can not handle this for now'
	return response
# 储存微信消息类型所对应函数（方法）的字典
msg_type_resp = {}


def set_msg_type(msg_type):
	"""
	储存微信消息类型所对应函数（方法）的装饰器
	"""
	def decorator(func):
		msg_type_resp[msg_type] = func
		return func
	return decorator


@set_msg_type('text')
def text_resp():
	"""文本类型回复"""
	# 默认回复微信消息
	response = 'success'
	# 替换全角空格为半角空格
	message.content = message.content.replace(u'　', ' ')
	# 清除行首空格
	message.content = message.content.lstrip()
	# 指令列表
	commands = {
		u'开启红灯':	red_led_on,
        u'关闭红灯':	red_led_off
	}
	# 匹配指令
	command_match = False
	for key_word in commands:
		if re.match(key_word, message.content):
			# 指令匹配后，设置默认状态
			response = commands[key_word]()
			command_match = True
			break
	if not command_match:
		response = command_not_found()
	return response

@set_msg_type('event')
def click_resp():
	"""菜单点击类型回复"""
	# 默认回复微信消息
	response = 'success'
	commands = {
		'red_led_on': red_led_on,
        'red_led_off': red_led_off
	}
	# 匹配指令后，重置状态
	if message.event == 'click':
		response = commands[message.key]()
	if message.event == 'subscribe':
		articles = [
			{
				'title': '微电网智能监控系统',
				'description': '微电网系统图',
				'image': 'http://www.imjiaofu.com:5588/static/img/sxpi/thumb.png',
				'url': 'http://www.imjiaofu.com:5588/sxpi'
			},
		]
		response = articles
	return response

def command_not_found():
	"""非关键词回复"""
	return u"未识别指令！\n"
    
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
        
class Wechat_view(MethodView):
	methods = ['GET', 'POST']
	def get(self):
		if self.IsAuthenticated():
			echo_str = request.args.get('echostr', '')
			return echo_str
		else:
			abort(403)
	def post(self):
		if self.IsAuthenticated():
			msg = parse_message(request.data)
			# POST request
			encrypt_type = request.args.get('encrypt_type', 'raw')
			if encrypt_type == 'raw':
				# plaintext mode
				response = wechat_response(msg)
				reply = create_reply(response, msg)
			else:
				# encryption mode
				reply = create_reply('Sorry, can not handle this for now', msg)
			return reply.render()
		else:
			abort(403)
	def IsAuthenticated(self):
		signature = request.args.get('signature', '')
		timestamp = request.args.get('timestamp', '')
		nonce = request.args.get('nonce', '')
		msg_signature = request.args.get('msg_signature', '')
		try:
			check_signature(app.config["TOKEN"], signature, timestamp, nonce)
		except InvalidSignatureException:
			return False;
		return True;
wechat_view = Wechat_view.as_view('wechat_view')
app.add_url_rule('/wechat', view_func=wechat_view,methods=['GET', 'POST'])
