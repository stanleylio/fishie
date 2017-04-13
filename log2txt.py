# store stuff from zmq to text file, with timestamps
# 
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved, 2017
import sys
from os.path import exists,join
from datetime import datetime
from helper import dt2ts
from config.config_support import import_node_config
from zmqloop import zmqloop


# product of this script: the raw text file
config = import_node_config()
output_path = getattr(config,'log2txt_output_path',None)
assert output_path is not None and exists(output_path)

with open(join(output_path,'raw.txt'),'a',0) as raw,\
     open(join(output_path,'tsraw.txt'),'a',0) as tsraw:

    def callback(m):
        print('= = = = = = = = = =')
        print(m)

        raw.write(m + '\n')
        dt = datetime.utcnow()
        tsraw.write('{}\t{:6f}\t{}\n'.format(dt.isoformat(),dt2ts(dt),m.strip()))

        raw.flush()
        tsraw.flush()

    zmqloop(callback)
