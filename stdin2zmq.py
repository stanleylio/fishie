import fileinput,argparse,zmq


parser = argparse.ArgumentParser(description="""Redirect STDIN to zmq.
Example: python stdin2zmq.py --port 127.0.0.1:9002""")
parser.add_argument('--port',dest='zmq_port',default=['127.0.0.1:9002'],type=str,nargs='+',
                    metavar='PORT',help='zmq port to subscribe to. Default = 127.0.0.1:9002')
args,unk = parser.parse_known_args()    # resolve conflict between argparse and fileinput


# ZMQ IPC stuff
context = zmq.Context()
zsocket = context.socket(zmq.PUB)
zsocket.bind('tcp://' + args.zmq_port[0])

for line in fileinput.input(unk):
    zsocket.send(line)
