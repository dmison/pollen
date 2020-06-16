import json
import tornado
# import unicode
from tornado.escape import _unicode


class Handler(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')

    def emit(self, data, event=None):
        """
        Actually emits the data to the waiting JS
        """
        response = u''
        encoded_data = json.dumps(data)
        if event is not None:
            response += u'event: ' + _unicode(event).strip() + u'\n'

        response += u'data: ' + encoded_data.strip() + u'\n\n'

        self.write(response)
        self.flush()
