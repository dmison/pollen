import os.path
from tornado import httpserver, ioloop, web
from tornado.options import define, options
from tornadose.handlers import EventSource
from tornadose.stores import QueueStore

store = QueueStore()

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode", type=bool)


class AddHandler(web.RequestHandler):

    async def post(self):
        store.submit(self.request.body)


if __name__ == "__main__":
    options.parse_command_line()
    static_path = os.path.abspath(
        "static/"
    )
    app = web.Application(
        debug=options.debug,
        handlers=[
            (r"/add", AddHandler),
            (r"/events", EventSource, {'store': store}),
            (r"/(index\.html)", web.StaticFileHandler, dict(path=static_path)),
        ]
    )

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
