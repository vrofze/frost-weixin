# encoding: utf-8
from tuling import getHtml
import json

def get(str):
    api = "http://fanyi.youdao.com/openapi.do?keyfrom=frostwx&key=594129755&type=data&doctype=json&version=1.1&q=%s" % str.encode('utf8')
    response = getHtml(api)
    dic_json = json.loads(response)
    res = ''
    code = dic_json["errorCode"]
    if code != 0:
        res += u"发生错误\n"
        if code == 20:
            res += u"要翻译的文本过长\n"
        elif code == 30:
            res += u"无法进行有效的翻译"
        elif code == 40:
            res += u"不支持的语言类型\n"
        elif code == 50:
            res += u"无效的ey\n"
        elif code == 60:
            res += u"无词典结果，仅在获取词典结果生效\n"
    else:
        res += dic_json["query"] + ":\n"
        for c in dic_json["translation"]:
            res += c + ","
        res = res[:-1] + "\n"
        res += u"------基本词典------\n"
        for c in dic_json["basic"]:
            res += c + ':'
            #if type(dic_json["basic"][c]) is dict:
            if type(dic_json["basic"][c]) is list:
                for cb in dic_json["basic"][c]:
                    res += cb + ","
                res = res[:-1] + "\n"
            else:
                res += dic_json["basic"][c] + "\n"
            #else:
            #    res += dic_json["basic"][c] + "\n"
        #if dic_json["basic"]["phonetic"] != "":
        #    res += u"国际:" + dic_json["basic"]["phonetic"] + "\n"
        #if dic_json["basic"]["uk-phonetic"] != "":
        #    res += u"英音:" + dic_json["basic"]["uk-phonetic"] + "\n"
        #if dic_json["basic"]["us-phonetic"] != "":
        #    res += u"美音:" + dic_json["basic"]["us-phonetic"] + "\n"
        #res += u"翻译:\n"
        #for c in dic_json["basic"]["explains"]:
        #    res += c + ","
        #res = res[:-1] + "\n"
        res += u"------网络释义-------\n"
        for c in dic_json["web"]:
            res += c["key"] + ":"
            for v in c["value"]:
                res += v + ","
            res = res[:-1] + "\n"
    return res


