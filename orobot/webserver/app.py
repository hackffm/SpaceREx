import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import serial
import thread
import pygame

ser = serial.Serial('/dev/ttyS0', 9600)
print(ser.name)
pygame.mixer.init(44100, -16, 1, 1024)

def readSerial():
	while True:
		data = ser.read();
		print 'from Arduino: ', data
		# received from Arduino written to all WebSocket clients
		[con.write_message(data) for con in WebSocketHandler.connections]


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	connections = set()

	def open(self):
		self.connections.add(self)
		print 'new connection was opened'
        	pass

	def on_message(self, message):
		print 'from WebSocket: ', message
		if(message[0] == 's'):
			#pygame.mixer.music.load("samples/321967__n-audioman__sheep-bleat.wav")
			pygame.mixer.music.load("samples/4913__noisecollector__cat1.wav")
			pygame.mixer.music.play()
		else:
			ser.write(message);	# received from WebSocket writen to arduino

	def on_close(self):
		self.connections.remove(self)
		print 'connection closed'
        	pass

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler),
	    (r'/(.*)', tornado.web.StaticFileHandler, {'path': './root'})
        ]

        settings = {
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ser.flushInput()
    thread.start_new_thread(readSerial, ())
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(9090)
    tornado.ioloop.IOLoop.instance().start()
