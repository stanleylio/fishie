import time,sqlite3
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. December 2015

if '__main__' == __name__:
    table = 'node_011'
    cols = ['Timestamp','T_180','T_5803','T_9808']

    print 'From sensor_data.db reading {}...'.format(table)
    cmd = 'SELECT {cols} FROM {table}'.format(cols=','.join(cols),table=table)

    dbfile = 'sensor_data.db'
    conn = sqlite3.connect(dbfile,\
                                detect_types=sqlite3.PARSE_DECLTYPES |\
                                sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute(cmd)
    dat = c.fetchall()

    # convert Python datetime objects to POSIX timestamps
    vals = [list(r) for r in zip(*dat)]
    vals[0] = [time.mktime(t.timetuple()) for t in vals[0]]
    #vals[1] = [time.mktime(t.timetuple()) for t in vals[1]]
    dat = zip(*vals)
    
    print 'Writing to file...'
    with open('{}.csv'.format(table),'w',0) as f:
        f.write(','.join(cols) + '\n')

        for r in dat:
            f.write(','.join([str(t) for t in r]) + '\n')
            
    print 'Done.'

