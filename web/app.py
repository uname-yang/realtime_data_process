import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import redis


from tornado.options import define, options
define("port", default=5000, help="run on the given port", type=int)

db = redis.Redis(host='redis',port=6379,db=0)

class Index(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',
        langs=[{
        "name":"python",
        "count":db.get('python')
        },{
        "name":"ruby",
        "count":db.get('ruby')
        },{
        "name":"javascript",
        "count":db.get('javascript')
        },{
        "name":"c",
        "count":db.get('c')
        },{
        "name":"perl",
        "count":db.get('perl')
        },{
        "name":"nodejs",
        "count":db.get('nodejs')
        }],
        tweets=[{
        "user":db.get('tw:python:img'),
        "tw":db.get('tw:python')
        },{
        "user":db.get('tw:ruby:img'),
        "tw":db.get('tw:ruby')
        },{
        "user":db.get('tw:javascript:img'),
        "tw":db.get('tw:javascript')
        },{
        "user":db.get('tw:scala:img'),
        "tw":db.get('tw:scala')
        },{
        "user":db.get('tw:c:img'),
        "tw":db.get('tw:c')
        },{
        "user":db.get('tw:nodejs:img'),
        "tw":db.get('tw:nodejs')
        }])

class Status(tornado.web.RequestHandler):
    def get(self,tag):
        count=db.get(tag)
        self.write(json.dumps(count))

class Tweets(tornado.web.RequestHandler):
    def post(self):
        lang = self.get_argument('lang', 'python')
        self.write(json.dumps(db.get('tw:'+lang)))

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/', Index),(r'/tweets', Tweets),(r'/status/(.*)',Status)],
		template_path=os.path.join(os.path.dirname(__file__), "tpl"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
