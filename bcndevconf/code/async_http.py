
import tornado.ioloop
import tornado.web
import tornado.httpclient
import urllib

URL = "https://whs.cartodb.com/api/v1/sql/"
QUERY= "select the_geom,name from whs_features where ST_Distance(the_geom::geography, ST_PointFromText('POINT(%f %f)', 4326)::geography) < 20000 LIMIT 20"

class APIHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        lat = float(self.get_argument('lat'))
        lon = float(self.get_argument('lon'))
        p = urllib.urlencode({'q': QUERY % (lon, lat)})
        http.fetch(URL + '?' + p,
                   callback=self.async_callback(self.on_response))

    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write({"places": [x['name'] for x in json["rows"]]})
        self.finish()

application = tornado.web.Application([
    (r"/api", APIHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
