import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import redis


from tornado.options import define, options
define("port", default=5000, help="run on the given port", type=int)

from cassandra.cluster import Cluster
from cassandra.query import dict_factory

cluster = Cluster(['cassandra'],port=9042)
session = cluster.connect()

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
        }])

class Status(tornado.web.RequestHandler):
    def get(self,tag):
        count=db.get(tag)
        self.write(json.dumps(count))

class Tweets(tornado.web.RequestHandler):
    def post(self):
        lookback =  request.args.get('lookback', 10)
        session.set_keyspace('twitter')
        session.row_factory = dict_factory
        date_time = datetime.datetime.now() - datetime.timedelta(minutes=int(lookback))
        date_str = date_time.strftime("%Y-%m-%d %H:%M:%S-0000")
        rows = session.execute("select id, title,lat,lon, location, profile_image_url from tweets where id >= maxTimeuuid('{0}') and id_str = 'id_str'".format(date_str))
        self.write(json.dumps(rows))

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
