# -*- coding: utf-8 -*-

from . import main
from flask import request, make_response
import hashlib
import xml.etree.ElementTree as ET
import time


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        token = 'imok'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        return make_response(echostr)
        if(hashlib.sha1(s).hexdigest == signature):
            return make_response(echostr)
    xml_recv = ET.fromstring(request.data)
    ToUserName = xml_recv.find('ToUserName').text
    FromUserName = xml_recv.find('FromUserName').text
    querystr = xml_recv.find('Content').text.encode('utf8')
    content = querystr  # distrib(querystr)
    reply = '<xml><ToUserName><![CDATA[%s]]></ToUserName>'
    '<FromUserName><![CDATA[%s]]></FromUserName>'
    '<CreateTime>%s</CreateTime>'
    '<MsgType><![CDATA[text]]></MsgType>'
    '<Content><![CDATA[%s]]></Content>'
    '<Funcflag>0</Funcflag></xml>'
    response = make_response(
        reply % (FromUserName, ToUserName, str(int(time.time())), content)
    )
    return response


@main.route('/hello', methods=['GET', 'POST'])
def hello():
    return 'Hello world!:p'
