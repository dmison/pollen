import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from SSE import Handler
from tornado.iostream import StreamClosedError
import asyncio

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode", type=bool)


class IndexHandler(tornado.web.RequestHandler):
    async def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')


class EventHandler(Handler.Handler):
    async def get(self):
        while True:
            try:
                self.emit('hello', 'there')
                await asyncio.sleep(1)
            except StreamClosedError:
                pass


if __name__ == "__main__":
    tornado.options.parse_command_line()
    static_path = os.path.abspath(
        "static/"
    )
    app = tornado.web.Application(
        debug=options.debug,
        handlers=[
            (r"/rest/(.*)", IndexHandler),
            (r"/date", EventHandler),
            (r"/(index\.html)", tornado.web.StaticFileHandler, dict(path=static_path)),

        ]
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
