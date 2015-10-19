import MySQLdb
from flask import Flask, g, request, make_response
import hashlib
import xml.etree.ElementTree as ET
import time

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
    if request.method == 'POST':
        xml_recv = ET.fromstring(request.data)
        ToUserName = xml_recv.find("ToUserName").text
        FromUserName = xml_recv.find("FromUserName").text
        Content = xml_recv.find("Content").text
        reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName>ToUserName><FromUserName><![CDATA[%s]]></FromUserName>FromUserName><CreateTime>%s</CreateTime>CreateTime><MsgType><![CDATA[text]]></MsgType>MsgType><Content><![CDATA[%s]]></Content>Content><FuncFlag>0</FuncFlag>FuncFlag></xml>xml>"
        response = make_response(reply % (FromUserName, ToUserName, str(int(time.time())), Content))
        response.content_type = 'application/xml'
        return response
