#-*- coding: utf-8 -*-
import MySQLdb
from flask import Flask, g, request, make_response
import hashlib
import xml.etree.ElementTree as ET
import time
import tuling
import youdao

app = Flask(__name__)
app.debug = True

from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

@app.route('/', methods = ['GET', 'POST'])
def wechat_auth():
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
        if(hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    xml_recv = ET.fromstring(request.data)
    ToUserName = xml_recv.find("ToUserName").text
    FromUserName = xml_recv.find("FromUserName").text
    querystr = xml_recv.find("Content").text.encode('utf8')
    Content = distrib(querystr)
    reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    response = make_response(reply % (FromUserName, ToUserName, str(int(time.time())), Content))
    response.content_type = 'application/xml'
    return response

def distrib(str):
    strt = str.decode('utf8')
    if strt[0:3] == u"翻译：" or strt[0:3] == u"翻译:" or strt[0:3] == 'fy:' or strt[0:3] == 'fy：':
        return youdao.get(strt[0:-3])
    else:
        return tuling.Get(str)
