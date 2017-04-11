import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import redis


from tornado.options import define, options
define("port", default=5000, help="run on the given port", type=int)

status_success = {
        "status": True
        }

class Index(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class Status(tornado.web.RequestHandler):
    def get(self):
        count=self.application.db.get("python:totals")
        print "OK:"+count

class Mess(tornado.web.RequestHandler):
	def post(self):
		tar = self.get_argument('url')
        producer.send('my-topic',tar)
        self.write(json.dumps(status_success))

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/', Index),(r'/tweets/(.*)', Mess),(r'/status/(.*)',Status)],
		template_path=os.path.join(os.path.dirname(__file__), "tpl"),
        static_path=os.path.join(os.path.dirname(__file__), "static")
        self.db = redis.Redis(host='redis',port=6379,db=0)
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
