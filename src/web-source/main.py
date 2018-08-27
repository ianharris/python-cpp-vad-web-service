from flask import Flask

# import the app
from server import app

# import python logging & RotatingFileHander
import logging
from logging.handlers import RotatingFileHandler

import iharrisvad as ihv

@app.route('/health-check')
def healthcheck():
    return 'OK'

from tornado.websocket import WebSocketHandler
class WebSocket(WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # need to track when we first notice voice
        self.voicedetected = False
        self.currentindex = 0

        ihv.setsamplerate(16000)
        ihv.setmode(2)

    def open(self):
        print("Socket opened.")

    def on_message(self, message):

        # initialise a response object
        rsp = {}

        # call the vad checker
        vad = (ihv.process(message) == 1)

        if vad and not self.voicedetected:
            self.voicedetected = True
            rsp['startindex'] = self.currentindex

        # return the result
        if vad or not self.voicedetected:
            rsp['moredata'] = True
        else:
            rsp['moredata'] = False
            rsp['stopindex'] = self.currentindex
        
        self.write_message(rsp)
        
        self.currentindex = self.currentindex + 1
        
    def on_close(self):
        print("Socket closed: {} - {}".format(self.close_code, self.close_reason))

if __name__ == '__main__':

    # initialize the log handler
    logHandler = RotatingFileHandler('./app.log', maxBytes=500000, backupCount=5)
    
    # set the log handler level
    logHandler.setLevel(logging.DEBUG)

    # set the app logger level
    app.logger.setLevel(logging.DEBUG)

    # add handler
    app.logger.addHandler(logHandler)

    # import tornado requirements
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.web import Application, FallbackHandler
    from tornado.ioloop import IOLoop
    
    container = WSGIContainer(app)
    server = Application([
        (r'/websocket/', WebSocket),
        (r'.*', FallbackHandler, dict(fallback=container))
    ])
    server.listen(8080)
    print('Starting server on port 8080')
    IOLoop.current().start()


