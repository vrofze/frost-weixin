# -*- coding:utf-8 -*-
"""tools used in main.py"""

import os
import urllib.request
from urllib import parse
import json

def distrib(strl):
    """used to distribute messages"""

    if strl[0:3] == u"翻译:" or strl[0:3] == u"翻译:":
        return youdao(strl[3:])
    if strl[0:3] == u'fy ' or strl[0:3] == u'fy ':
        return youdao(strl[3:])
    else:
        return tuling(strl)


def get_html(url):
    """get api"""

    page = urllib.request.urlopen(url)
    html = page.read()
    return html


def tuling(strl):
    """tuling bot"""

    key = os.getenv('TULING_KEY')  # settings['tuling_key']
    strl = parse.quote(strl)
    api = "http://www.tuling123.com/openapi/api?key=%s&info=%s" % (key, strl)
    response = get_html(api)
    dic_json = json.loads(response.decode('utf8'))
    return dic_json['text']


def youdao(strl):
    """youdao dict"""

    strl = parse.quote(strl)
    api = "http://fanyi.youdao.com/openapi.do?"\
          "keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=%s" \
          % (os.getenv('YOUDAO_USER'), os.getenv('YOUDAO_KEY'), strl)
    response = get_html(api)
    dic = json.loads(response.decode('utf8'))
    err_dic = {
        20: u'要翻译的文本过长',
        30: u'无法进行有效的翻译',
        40: u'不支持的语言类型',
        50: u'无效的key',
        60: u'无词典结果'
    }
    if dic['errorCode'] != 0:
        return err_dic[dic['errorCode']]
    res = get_str(dic)
    print(res)
    return res


def get_str(dic):
    """get str from dic"""
    res = dic['query'] + ":\n"
    res += getlist(dic['translation']) + "\n"
    if 'basic' in dic.keys():
        res += '------基本词典------\n'
        for k, v in dic['basic'].items():
            res += transl(k) + getlist(v) + "\n"
    if 'web' in dic.keys():
        res += '------网络词典------\n'
        for c in dic['web']:
            res += getlist(c['key']) + ":"
            res += getlist(c['value']) + ";\n"
    return res


def getlist(li):
    """ get str from list"""
    res = ''
    if isinstance(li, list):
        for v in li:
            res += getlist(v) + ','
        res = res[0:-1]
    elif isinstance(li, str):
        res += li
    else:
        return li
    return res

transl_dic = {
    'basic': '-----基本词典-----\n',
    'web': '-----网络释意-----\n',
    'phonetic': '发音:',
    'uk-phonetic': '英式发音:',
    'us-phonetic': '美式发音:',
    'explains': '解释:',
    'key': '',
    'value': ''
    }

def transl(strl):
    """translate english tag to chinese"""
    if strl in transl_dic.keys():
        return transl_dic[strl]
    return str


"""
def store(str, param=tuple()):
    helper = mysqlhelper(host='localhost', user='user', passwd='XXX', db='weixin')
    return helper.query(str, param)
"""
