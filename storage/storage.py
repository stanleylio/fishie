#!/usr/bin/python
#
# Cleaned up the structure a bit...
# but avg() is nice though.
#
# Stanley Hou In Lio, hlio@hawaii.edu
# October, 2015

import sqlite3,sys
from os.path import join,dirname
from datetime import timedelta


def PRINT(s):
    #pass
    print(s)


# this one doesn't require you to supply the database schema
class storage_read_only(object):
    def __init__(self,dbfile=None):
        if dbfile is None:
            dbfile = join(dirname(__file__),'sensor_data.db')
        self.conn = sqlite3.connect(dbfile,\
                                    detect_types=sqlite3.PARSE_DECLTYPES |\
                                    sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        self.c.execute('PRAGMA journal_mode = WAL')
        self.c.row_factory = sqlite3.Row

    def get_list_of_tables(self):
        cursor = self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return sorted(tuple(t[0] for t in cursor.fetchall()))

    def get_list_of_columns(self,node_id):
        cursor = self.c.execute('SELECT * FROM node_{:03d};'.format(node_id))
        return [d[0] for d in cursor.description]

    def read_time_range(self,node_id,time_col,cols,timerange):
        assert type(node_id) is int,'storage::read_time_range(): node_id must be int'
        assert type(cols) is list,'storage::read_time_range(): cols must be a list of string'
        #if 'Timestamp' not in cols and 'ReceptionTime' not in cols:
        #    print('Sure you don''t need any timestamps?')

        nday = timerange.days
        nhour = timerange.seconds//3600
        nmin = (timerange.seconds//60)%60

        tmp = ['"now"']
        tmp.append('"-{} minutes"'.format(nmin))
        tmp.append('"-{} hours"'.format(nhour))
        tmp.append('"-{} days"'.format(nday))
        time_range = 'WHERE {} >= DATETIME({})'.format(time_col,','.join(tmp))
        #print time_range

        cmd = 'SELECT {} FROM {} {} ORDER BY {} DESC'.\
                format(','.join(cols),
                       'node_{:03d}'.format(node_id),
                       time_range,
                       time_col)
        #print cmd
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        try:
            return {v:tuple(r[v] for r in tmp) for v in cols}
        except:
            return None
        #vals = [tuple(r) for r in zip(*tmp)]
        #tmp = dict(zip(cols,vals))
        #if len(tmp.keys()) <= 0:
        #    tmp = None
        #return tmp

    def read_last_N(self,node_id,time_col,count,cols=None):
        assert type(node_id) is int,'storage::read_last_N(): node_id must be int'
        assert cols is None or type(cols) is list,'storage::read_last_N(): cols, if not None, must be a list of string'
        if cols is not None:
            if 'Timestamp' not in cols and 'ReceptionTime' not in cols:
                print('Sure you don''t want any timestamps?')

        if cols is None:
            cols = self.get_list_of_columns(node_id)

        cmd = 'SELECT {} FROM {} ORDER BY {} DESC LIMIT {}'.\
                format(','.join(cols),
                       'node_{:03d}'.format(node_id),
                       time_col,
                       count)
        #print cmd
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        try:
            return {v:tuple(r[v] for r in tmp) for v in cols}
        except:
            return None
        #vals = [tuple(r) for r in zip(*tmp)]
        #tmp = dict(zip(cols,vals))
        #if len(tmp.keys()) <= 0:
        #    tmp = None
        #return tmp


class storage(storage_read_only):
    def __init__(self,schema,dbfile=None):
        super(storage,self).__init__(dbfile=dbfile)

        self._schema = schema
        #print self._schema
        
        for node_id,v in self._schema.iteritems():
            table_name = 'node_{:03d}'.format(node_id)
            dbtag = v['tag']
            dbtype = v['type']
            tmp = '({})'.format(','.join([' '.join(p) for p in zip(dbtag,dbtype)]))
            cmd = 'CREATE TABLE IF NOT EXISTS {} {}'.format(table_name,tmp)
            self.c.execute(cmd)
    
    # Three cases:
    #   More keys than columns
    #       Filter out keys not in the database
    #   The set of keys matches the set of columns
    #   More columns than keys
    #       Handled by the database - missing fields are replaced by NULLs
    def write(self,node_id,readings):
        assert self._schema is not None
        assert 'ReceptionTime' in readings.keys() or 'Timestamp' in readings.keys()

        if len(readings.keys()) > len(self._schema[node_id]['tag']):
            PRINT('storage.py::write(): Warning: some supplied readings are not defined in the db')
            PRINT('Expected:')
            PRINT(','.join(sorted(self._schema[node_id]['tag'])))
            PRINT('Supplied:')
            PRINT(','.join(sorted(readings.keys())))
        
        # filter out readings that are not recorded by the database
        keys = [k for k in readings.keys() if k in self._schema[node_id]['tag']]
        vals = [readings[k] for k in keys]
        table_name = 'node_{:03d}'.format(node_id)
        cmd = 'INSERT OR REPLACE INTO {} ({}) VALUES ({})'.\
              format(table_name,','.join(keys),','.join('?'*len(keys)))

        self.c.execute(cmd,vals)
        self.conn.commit()


if '__main__' == __name__:

    node_id = 7
    time_col = 'Timestamp'
    cols = ['Timestamp','Temp_BMP180','Wind_average']

    s = storage_read_only()
    print s.read_last_N(node_id,time_col,cols,5)
    print
    print s.read_time_range(node_id,time_col,cols,timedelta(days=0,minutes=5))
    print

    import config
    from config.config_support import read_capabilities
    s = storage(read_capabilities())
    

    
    
