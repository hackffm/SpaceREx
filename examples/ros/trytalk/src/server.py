#!/usr/bin/env python
import os

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import threading, Queue

import rospy
from std_msgs.msg import String

NODE_NAME = 'webserver_node'
messageToRos = Queue.Queue()
messageFromRos = Queue.Queue()

currenPath = os.path.dirname(os.path.abspath(__file__))
resourcesPath = currenPath + '/ressources'

def cb_writeToSocket(data):
    rosInput = data.data
    rospy.loginfo('send to websockets %s', rosInput)
    messageFromRos.put(rosInput)
    [con.write_message(rosInput) for con in WebSocketHandler.connections]

def readMessageFromRos(messageFromROS):
    print('init fromRos_topic')
    rospy.Subscriber('fromRos_topic', String, cb_writeToSocket)

def writeMessageToRos(messageToRos):
    print ('init fromWebserver_topic')
    pub = rospy.Publisher('fromwebserver_topic', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        msg = messageToRos.get()
	rospy.loginfo('new messageToRos: %s', msg)
        pub.publish(msg)
        rate.sleep()

class WebSocketHandler(tornado.websocket.WebSocketHandler):
        connections = set()

        def open(self):
                self.connections.add(self)
                print 'new connection was opened'
                pass

        def on_message(self, message):
                print 'from WebSocket: ', message
                messageToRos.put(message)

        def on_close(self):
                self.connections.remove(self)
                print 'connection closed'
                pass

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class webApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': resourcesPath})
        ]

        settings = {
            'static_path': resourcesPath,
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
        print('init ' + NODE_NAME)
	rospy.init_node(NODE_NAME, anonymous=True)

	threadSocketsToRos = threading.Thread(target=writeMessageToRos,args=(messageToRos, ))
	threadRosToSockets = threading.Thread(target=readMessageFromRos,args=(messageFromRos, ))
        threadSocketsToRos.start()
        threadRosToSockets.start()

    	ws_app = webApplication()
    	server = tornado.httpserver.HTTPServer(ws_app)
    	server.listen(9090)
    	tornado.ioloop.IOLoop.instance().start()
