import os.path
from json.decoder import JSONDecodeError

from tornado import httpserver, ioloop, web, escape
from tornado.options import define, options
from tornadose.handlers import EventSource
from tornadose.stores import QueueStore
import jwt

store = QueueStore()

define("port", default=3000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode", type=bool)

public_key = open(os.path.abspath("id_rsa.pub"), "r").read()
private_key = open(os.path.abspath("id_rsa"), "r").read()


class ESHandler(EventSource):
    # def write_error(self, status_code, **kwargs):
    #     # e = kwargs["exc_info"]
    #     self.render("error.html")

    def get_current_user(self):
        token = self.path_args[0]
        print(token)

        try:
            token = jwt.decode(self.request.token, public_key, algorithm="RS256")
            return token.user
        except AttributeError:
            raise web.HTTPError(400, "invalid token or token missing")
        except jwt.exceptions.ExpiredSignatureError:
            raise web.HTTPError(401, "Token Expired")
        except Exception:
            raise web.HTTPError(401, "token authentication failed")

    @web.authenticated
    async def get(self, *args, **kwargs):
        super.get(self, args, kwargs)


class LoginHandler(web.RequestHandler):
    async def post(self):
        name = self.get_body_argument("name")
        token = jwt.encode({"user": name}, private_key, algorithm="RS256",)
        self.add_header("token", token)
        self.redirect("/")


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
    templates_path = os.path.abspath("templates/")
    app = web.Application(
        debug=options.debug,
        template_path=templates_path,
        handlers=[
            (r"/rest/v1/login", LoginHandler),
            (r"/sse/v1/events/add", AddHandler),
            (r"/sse/v1/events/listen/(.+)", ESHandler, {"store": store}),
            (
                r"/(.*)",
                web.StaticFileHandler,
                dict(path=static_path, default_filename="index.html"),
            ),
        ],
    )

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
