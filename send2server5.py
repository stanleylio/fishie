# Send a string to i7NUC via HTTP POST
# Messages are signed by the private key of this device
# Messages are verified by i7NUC with the public key of this device
#
# Targeted at the v4 API
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# University of Hawaii
# All Rights Reserved. 2016
import requests,sys,socket,time
from os.path import expanduser
sys.path.append(expanduser('~'))
from uhcmrt_cred import cred


if '__main__' == __name__:

    url = 'http://grogdata.soest.hawaii.edu/api/5/raw'

    ts = time.time()
    node = socket.gethostname()
    
    if len(sys.argv) > 1:
        M = sys.argv[1:]
    else:
        M = ['"beatings will continue until morale improves"']

    for m in M:
        r = requests.post(url,
                          data={'m':m,'ts':ts,'src':node},
                          auth=('uhcm',cred['uhcm']))
        print(r.text)
