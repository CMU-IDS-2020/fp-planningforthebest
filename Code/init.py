import tornado.ioloop
import tornado.web
import tornado.websocket
import os
from core import Core

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("main.html", error="", port=port)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
  def initialize(self, core):
    self.core = core
    core.set_websocket(self)

  def open(self):
    print("Web Socket Opened")

  def on_message(self, message):
    self.core.handle_message(message)

  def on_close(self):
    print('Web Socket Closed')



settings = dict(static_path=os.path.join(os.path.dirname(__file__), "static"))
port = 8888

if os.name == 'nt':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    io_loop = tornado.ioloop.IOLoop.current()
    core = Core()
    application = tornado.web.Application([
        (r'(?i)/', MainHandler),
        (r'(?i)', MainHandler),
        (r'(?i)/websocket', WebSocketHandler, {'core': core}),
        (r'(?i)/static/(.*)', tornado.web.StaticFileHandler, {'path': settings["static_path"]}),
    ], **settings)

    application.listen(port)
    io_loop.start()
    print("server start running on " + str(port))

