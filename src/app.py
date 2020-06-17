import os.path
from json.decoder import JSONDecodeError
from tornado import httpserver, ioloop, web, escape
from tornado.options import define, options
from tornadose.handlers import EventSource
from tornadose.stores import QueueStore

store = QueueStore()

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode", type=bool)


class AddHandler(web.RequestHandler):

    async def post(self):
        try:
            data = escape.json_decode(self.request.body)
            store.submit(escape.json_encode(data))
        except JSONDecodeError:
            raise web.HTTPError(400, "Invalid JSON")
        except Exception:
            raise web.HTTPError(500, "opps")


if __name__ == "__main__":
    options.parse_command_line()
    static_path = os.path.abspath("static/")
    app = web.Application(
        debug=options.debug,
        handlers=[
            (r"/add", AddHandler),
            (r"/events", EventSource, {'store': store}),
            (r"/(.*)",
                web.StaticFileHandler,
                dict(path=static_path, default_filename="index.html")),
        ]
    )

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
