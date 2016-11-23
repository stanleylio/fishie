# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2016
import os,time,json,sys,traceback,zmq
import logging.handlers
sys.path.append(r'/home/nuc/node')
from twisted.internet.task import LoopingCall
from twisted.internet import reactor


# ZMQ IPC stuff
topic = u''
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://127.0.0.1:9002')
socket.setsockopt_string(zmq.SUBSCRIBE,topic)

poller = zmq.Poller()
poller.register(socket,zmq.POLLIN)

def taskListener():
    try:
        socks = dict(poller.poll(100))
        if socket in socks and zmq.POLLIN == socks[socket]:
            m = socket.recv()
            print m
    except:
        logger.debug(traceback.format_exc())



LoopingCall(taskListener).start(0.01,now=True)

reactor.run()

socket.close()
