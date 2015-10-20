#-*- coding:utf-8 -*-
import urllib
import json

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def Get(str):
    key = "4ee47c1278c5cada2e82cf36861ffb2a"
    api = "http://www.tuling123.com/openapi/api?key=%s&info=%s" % (key, str)
    response = getHtml(api)
    dic_json = json.loads(response)
    return dic_json['text']
