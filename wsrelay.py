assert False
# who's using this?

import logging
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS


class BroadcastServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        '''if not isBinary:
            msg = "{} from {}".format(payload.decode('utf8'), self.peer)
            self.factory.broadcast(msg)'''
        pass

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            logging.debug("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            logging.debug("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        #logging.debug("broadcasting message '{}'".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            logging.debug("message sent to {}".format(c.peer))


if __name__ == '__main__':
    import sys
    from twisted.internet.task import LoopingCall

    ServerFactory = BroadcastServerFactory
    factory = ServerFactory(u"ws://*:9003")
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)

    def taskRelay():
        for line in sys.stdin:
            print(line)
            factory.broadcast(line.strip())
            
    LoopingCall(taskRelay).start(0.01)
    reactor.run()
