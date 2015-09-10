#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import sqlite3,sys
sys.path.append('../config')
from os.path import join,dirname,exists


def PRINT(s):
    #pass
    print(s)


# one table per node
# one column per variable
class storage(object):
    def __init__(self,schema=None,dbfile=None):
        if dbfile is None:
            dbfile = join(dirname(__file__),'sensor_data.db')
        self.conn = sqlite3.connect(dbfile,\
                                    detect_types=sqlite3.PARSE_DECLTYPES |\
                                    sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        self.c.execute('PRAGMA journal_mode = WAL')
        self.c.row_factory = sqlite3.Row
        self._schema = schema

        if self._schema is not None:
            for node_id,v in self._schema.iteritems():
                table_name = 'node_{:03d}'.format(node_id)
                dbtag = v['tag']
                dbtype = v['type']
                tmp = '({})'.format(','.join([' '.join(p) for p in zip(dbtag,dbtype)]))
                cmd = 'CREATE TABLE IF NOT EXISTS {} {}'.format(table_name,tmp)
                self.c.execute(cmd)

# three cases:
#   more keys than columns [keys not in the db are filtered out]
#   set of keys matches set of columns
#   more columns than keys  [handled by the db, missing values stored as NULL]
    def write(self,node_id,readings):
        assert self._schema is not None
        assert 'ReceptionTime' in readings.keys() or 'Timestamp' in readings.keys()

        # filter out readings that are not recorded by the database
        keys = [k for k in readings.keys() if k in self._schema[node_id]['tag']]
        vals = [readings[k] for k in keys]
        table_name = 'node_{:03d}'.format(node_id)
        cmd = 'INSERT OR REPLACE INTO {} ({}) VALUES ({})'.\
              format(table_name,','.join(keys),','.join('?'*len(keys)))

        self.c.execute(cmd,vals)
        self.conn.commit()


# hum... may as well make this read-only. All this mess just to support plotting.
# if this is read-only __init__() doesn't even need the capabilities
# TODO
class storage_rw(storage):
    def read_latest(self,node_id,time_col,variables,count=1):
        """retrieve the last "count" readings"""
        return self.read(node_id,time_col=time_col,variables=variables,count=count)

#    def read_all(self,node_id,col_name=None):
#        return self.read(node_id,variables=col_name)

#    def hourly_average(self,node_id,col_name=None,time_col=None):
#        """read hourly averages (all time)"""
#        return self.read(node_id,variables=col_name,time_col=time_col,avg='hourly')

#    def daily_average(self,node_id,col_name=None,time_col=None):
#        """read daily averages (all time)"""
#        return self.read(node_id,variables=col_name,time_col=time_col,avg='daily')

    def WHAT_____________read_time_range(self,node_id,time_col=None):
        """return the earliest and latest timestamps in a list"""
        if time_col is None:
            if 'Timestamp' in self._capability[node_id]['tag']:
                # only the BBB nodes have Timestamp
                time_col = 'Timestamp'
            elif 'ReceptionTime' in self._capability[node_id]['tag']:
                # ReceptionTime is recorded only at the base station, but is available for all nodes
                time_col = 'ReceptionTime'
            else:
                raise Exception('Neither Timestamp nor ReceptionTime exists - not a time series database.')
        # this won't work. it gives you a string representation of the time instead (don't ask me why)
        #cmd = 'SELECT min(Timestamp) from node_003'
        cmd = '''SELECT {time_col} FROM node_{node_id:03d} where {time_col} in 
(select min({time_col}) from node_{node_id:03d})'''.format(node_id=node_id,time_col=time_col)
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        min_t = None
        if len(tmp) > 0:
            min_t = tmp[0][0]
        cmd = '''SELECT {time_col} FROM node_{node_id:03d} where {time_col} in 
(select max({time_col}) from node_{node_id:03d})'''.format(node_id=node_id,time_col=time_col)
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        max_t = None
        if len(tmp) > 0:
            max_t = tmp[0][0]
        return [min_t,max_t]
    
    def read(self,node_id,time_col,variables,nhour=None,nday=None,count=None,avg=None):
        """retrieve samples of a given node for a given duration

        variables: a list of names of the columns to retrieve
        time_col: specifies which of the column is the time column
        nhour: when specified, retrieve only the last "nhour" hours of data (work with nday)
        nday: when specified, retrieve only the last "nday" days of data (work with nhour)
        count: when specified, retrieve the last "count" entries
        avg: one of {'hourly','daily'}. When specified, return the data as "avg" averages.
        """
        assert type(node_id) is int,'storage::read(): node_id must be int'
        assert nhour is None or nhour >= 0
        assert nday is None or nday >= 0
        assert count is None or count >= 1

        '''# auto select time_col:
        # use Timestamp if it exists; otherwise use ReceptionTime
        if time_col is None:
            if 'Timestamp' in self._schema[node_id]['tag']:
                # only the BBB nodes have Timestamp
                time_col = 'Timestamp'
            elif 'ReceptionTime' in self._schema[node_id]['tag']:
                # ReceptionTime is recorded only at the base station, but is available for all nodes
                time_col = 'ReceptionTime'
            else:
                raise Exception('Neither Timestamp nor ReceptionTime exists - not a time series database.')'''

        if type(variables) is str:
            variables = [variables]
            
        '''# if the list of variables is not specified, retrieve all variables defined in the config
        if variables is None:
            variables = self._capability[node_id]['tag']
            variables = [c for c in variables if c != time_col]'''
        
        table_name = 'node_{:03d}'.format(node_id)

        orderby = 'ORDER BY {} DESC'.format(time_col)
        countlimit = ''
        if count >= 1:
            countlimit = 'LIMIT {}'.format(count)
        tmp = ['"now"']
        if nhour is not None:
            tmp.append('"-{} hours"'.format(nhour))
        if nday is not None:
            tmp.append('"-{} days"'.format(nday))
        if nday is not None or nhour is not None:
            time_range = 'WHERE {} >= DATETIME({})'.format(time_col,','.join(tmp))
        else:
            time_range = ''
        #print time_range

        if avg in ['hourly','daily']:
            # applies avg() on all columns except time_col
            tmp = ','.join(['avg({})']*len(variables))
            tmp = tmp.format(*variables)
            cols = '{},{}'.format(time_col,tmp)
            if 'hourly' == avg:
                groupby = 'GROUP BY strftime("%Y%m%d%H",{})'.format(time_col)
            elif 'daily' == avg:
                groupby = 'GROUP BY strftime("%Y%m%d",{})'.format(time_col)
        else:
            tmp = ','.join(variables)
            cols = '{},{}'.format(time_col,tmp)
            groupby = ''
        #print cols
        #print groupby
        #print orderby

        tmp = ['SELECT {cols} FROM {table_name}'.format(cols=cols,table_name=table_name),
               time_range,
               groupby,
               orderby,
               countlimit]
        cmd = ' '.join([c for c in tmp if len(c) > 0])
#        print cmd

        self.c.execute(cmd)
        tmp = self.c.fetchall()
        #vals = [list(r) for r in zip(*tmp)]
        vals = [tuple(r) for r in zip(*tmp)]
        # careful there... if list() is not used, the original would be modified
        #keys = list(variables)
        #keys.insert(0,time_col)    # this would modify the original if a copy was not made
        keys = [time_col]
        keys.extend(variables)
        tmp = dict(zip(keys,vals))
        if len(tmp.keys()) <= 0:
            tmp = None
        return tmp


if '__main__' == __name__:
    #from datetime import datetime
    from config_support import read_capabilities
    store = storage_rw(read_capabilities())
    #store.write(1,{'Timestamp':datetime.utcnow(),'Oxygen':123.456,'Temp_MS5803':99.9,'bug':32768})
    #exit()

    node_id = 3
    time_col = 'Timestamp'
    var = ['Temp_MS5803']

    print
    print 'read_latest()'
    tmp = store.read_latest(node_id,time_col,var,count=1)
    print tmp
    
    '''print
    print 'read_time_range()'
    tmp = store.read_time_range(node_id,time_col='Timestamp')
    print tmp
    print type(tmp[0])'''

    print
    print 'read max six entries (should have precedence over nhour)'
    tmp = store.read(node_id,time_col,var,nhour=10,count=6)
    print tmp

    print
    print 'hourly average of "{}" in the past 1 day, 3 hours'.format(var)
    tmp = store.read(node_id,time_col,var,nhour=3,nday=1,avg='hourly')
    print tmp.keys()
    print len(tmp[var[0]])

    '''print
    print 'daily average of the past 14 days, all variables'
    tmp = store.read(node_id,time_col,var,nday=14,avg='daily')
    print tmp.keys()
    print len(tmp[var[0]])

    print
    print 'past 6 hours, all variables'
    tmp = store.read(node_id,time_col,var,nhour=6)
    print tmp.keys()
    print len(tmp[var[0]])'''

    # read everything
#    tmp = store.read(node_id)
#    print
#    print tmp.keys()
#    print len(tmp[var])

#    tmp = store.read_all(node_id)
#    print
#    print tmp.keys()
#    print len(tmp[var])

