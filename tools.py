# -*- coding:utf-8 -*-
import urllib.request
from urllib import parse
import json
from setting import settings

def distrib(str):
    """used to distribute messages"""

    strt = str
    if strt[0:3] == u"翻译:" or strt[0:3] == u"翻译:":
        return youdao(strt[3:])
    if strt[0:3] == u'fy ' or strt[0:3] == u'fy ':
        return youdao(strt[3:])
    else:
        return tuling(str)


def getHtml(url):
    """get api"""

    page = urllib.request.urlopen(url)
    html = page.read()
    return html


def tuling(str):
    """tuling bot"""

    key = settings['tuling_key']
    str = parse.quote(str)
    api = "http://www.tuling123.com/openapi/api?key=%s&info=%s" % (key, str)
    response = getHtml(api)
    dic_json = json.loads(response.decode('utf8'))
    return dic_json['text']


def youdao(str):
    """youdao dict"""

    str = parse.quote(str)
    api = settings['youdao_api'] % str
    response = getHtml(api)
    dic = json.loads(response.decode('utf8'))
    err_dic = {
        '20': u'要翻译的文本过长',
        '30': u'无法进行有效的翻译',
        '40': u'不支持的语言类型',
        '50': u'无效的key',
        '60': u'无词典结果'
    }
    if dic['errorCode'] != 0:
        return err_dic[dic['errorCode']]
    res = getStr(dic)
    print(res)
    return res


def getStr(dic):
    res = dic['query'] + ":\n"
    res += getlist(dic['translation']) + "\n"
    if('basic' in dic.keys()):
        res += '------基本词典------\n'
        for k, v in dic['basic'].items():
            res += transl(k) + getlist(v) + "\n"
    if('web' in dic.keys()):
        res += '------网络词典------\n'
        for c in dic['web']:
            res += getlist(c['key']) + ":"
            res += getlist(c['value']) + ";\n"
    return res


def getlist(li):
    res = ''
    if(type(li) == list):
        for v in li:
            res += getlist(v) + ','
        res = res[0:-1]
    elif(type(li) == str):
        res += li
    else:
        return li
    return res

'''
def getStr(dic):
    res = ''
    if(type(dic) == dict):
        for k, v in dic.items():
            if(k == 'errorCode' or k == 'translation' or k == 'query'):
                continue
            res += transl(k)
            if(v != 'key'):
                res += getStr(v) + '\n'
    elif(type(dic) == list):
        for c in dic:
            res += getStr(c) + ';'
        res += '\n'
    elif(type(dic) == str):
        res += dic
    else:
        res += "error"
    return res
'''


def transl(str):
    dic = {
        'basic': '-----基本词典-----\n',
        'web': '-----网络释意-----\n',
        'phonetic': '发音:',
        'uk-phonetic': '英式发音:',
        'us-phonetic': '美式发音:',
        'explains': '解释:',
        'key': '',
        'value': ''
    }
    if(str in dic.keys()):
        return dic[str]
    return str


"""
def store(str, param=tuple()):
    helper = mysqlhelper(host='localhost', user='user', passwd='XXX', db='weixin')
    return helper.query(str, param)
"""
