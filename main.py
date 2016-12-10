"""
frost weixin web server by tornado
"""
import os
import time
import hashlib
import xml.etree.ElementTree as ET
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.wsgi
import gevent.wsgi
from tools import distrib

from tornado.options import define, options

define("port", default=8001, help="run on the given port", type=int)

class Application(tornado.wsgi.WSGIApplication): # tornado.web.Application
    """application from tornado.web.Application"""

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/test", TestHandler),
        ]

        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            # template_static=os.path.join(os.path.dirname(__file__), "static"),
        )

        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    """main handler"""

    def get(self):
        token = "imok"
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        str_list = [timestamp, nonce, token]
        str_list.sort()
        str_encode = ''.join(str_list).encode('utf8')
        if(hashlib.sha1(str_encode).hexdigest()==signature):
            self.write(echostr)
            return
        return

    def post(self):
        xml_recv = ET.fromstring(self.request.body.decode())
        to_user_name = xml_recv.find("ToUserName").text
        from_user_name = xml_recv.find("FromUserName").text
        query_str = xml_recv.find("Content").text
        content = distrib(query_str)
        reply = """
        <xml><ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        <FuncFlag>0</FuncFlag></xml>
        """
        self.write(reply % (from_user_name,
                            to_user_name,
                            str(int(time.time())),
                            content))


class TestHandler(tornado.web.RequestHandler):
    """test handler"""

    def get(self):
        self.write(":)")

def main():
    """app start point"""
    tornado.options.parse_command_line()
    # http_server = tornado.httpserver.HTTPServer(Application())
    # http_server.listen(options.port)
    # tornado.ioloop.IOLoop.current().start()
    server = gevent.wsgi.WSGIServer(('', 8001), Application())
    server.serve_forever()

if __name__ == "__main__":
    main()
