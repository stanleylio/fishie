#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import sqlite3
from os.path import join,dirname,exists


def PRINT(s):
    #pass
    print(s)

# one table per node
# one column per variable

class storage(object):
    def __init__(self,capability=None):
        tmp = join(dirname(__file__),'sensor_data.db')
        self.conn = sqlite3.connect(tmp,\
                                    detect_types=sqlite3.PARSE_DECLTYPES |\
                                    sqlite3.PARSE_COLNAMES)
        self.c = self.conn.cursor()
        self.c.execute('PRAGMA journal_mode = WAL')

        # auto vacuum? nah. costly.

        #def dict_factory(cursor,row):
        #    d = {}
        #    for idx,col in enumerate(cursor.description):
        #        d[col[0]] = row[idx]
        #    return d
        #self.c.row_factory = dict_factory
        self.c.row_factory = sqlite3.Row

        # "create table if not exist"
        if capability is not None:
            self._capability = capability
            
            for node_id in self._capability.keys():
                dbtag = self._capability[node_id]['dbtag']
                dbtype = self._capability[node_id]['dbtype']

                table_name = 'node_{:03d}'.format(node_id)
                schema = '({})'.format(','.join([' '.join(p) for p in zip(dbtag,dbtype)]))
                cmd = 'CREATE TABLE IF NOT EXISTS {} {}'.format(table_name,schema)
                self.c.execute(cmd)
        else:
            self._capability = {}
            
            self.c.execute('SELECT name FROM sqlite_master WHERE type = "table"')
            tmp = self.c.fetchall()
            node_ids = [int(c[0][5:8]) for c in tmp]

            for node_id in node_ids:
                #self.c.execute('SELECT * FROM node_{:03d}'.format(node_id))
                #self._capability[node_id] = {}
                #self._capability[node_id]['dbtag'] = [c[0] for c in self.c.description]

                self.c.execute('PRAGMA table_info(node_{:03d})'.format(node_id))
                tmp = zip(*[(c[1],c[2]) for c in self.c.fetchall()])
                self._capability[node_id] = {}
                self._capability[node_id]['dbtag'] = list(tmp[0])
                self._capability[node_id]['dbunit'] = list(tmp[1])

    # readings: a dictionary with keys=column names and vals=readings
    # as long as the caller supply all the required values
    # ignore the extra ones (such as Checksum, if exist)
    # what is "required" for each node is defined in the configuration file, "dbtag"
    def write(self,node_id,readings):
        table_name = 'node_{:03d}'.format(node_id)
        dbtag = self._capability[node_id]['dbtag']
        readings = [readings[v] for v in dbtag]
        cmd = 'INSERT OR REPLACE INTO {} ({}) VALUES ({})'.\
              format(table_name,','.join(dbtag),','.join('?'*len(dbtag)))
        self.c.execute(cmd,readings)
        self.conn.commit()

    def read_all(self,node_id,col_name=None):
        return self.read(node_id,variables=col_name)
        
    def read_latest(self,node_id,col_name=None,count=1,time_col=None):
        """retrieve the last "count" readings"""
        return self.read(node_id,variables=col_name,count=count,time_col=time_col)

    def hourly_average(self,node_id,col_name=None,time_col=None):
        """read hourly averages (all time)"""
        return self.read(node_id,variables=col_name,time_col=time_col,avg='hourly')

    def daily_average(self,node_id,col_name=None,time_col=None):
        """read daily averages (all time)"""
        return self.read(node_id,variables=col_name,time_col=time_col,avg='daily')

    def read_time_range(self,node_id,time_col=None):
        """return the earliest and latest timestamps in a list"""
        if time_col is None:
            if 'Timestamp' in self._capability[node_id]['dbtag']:
                # only the BBB nodes have Timestamp
                time_col = 'Timestamp'
            elif 'ReceptionTime' in self._capability[node_id]['dbtag']:
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
    
    def read(self,node_id,variables=None,time_col=None,nhour=None,nday=None,count=None,avg=None):
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

        # auto select time_col:
        # use Timestamp if it exists; otherwise use ReceptionTime
        if time_col is None:
            if 'Timestamp' in self._capability[node_id]['dbtag']:
                # only the BBB nodes have Timestamp
                time_col = 'Timestamp'
            elif 'ReceptionTime' in self._capability[node_id]['dbtag']:
                # ReceptionTime is recorded only at the base station, but is available for all nodes
                time_col = 'ReceptionTime'
            else:
                raise Exception('Neither Timestamp nor ReceptionTime exists - not a time series database.')

        # if the list of variables is not specified, retrieve all variables defined in the config
        if variables is None:
            variables = self._capability[node_id]['dbtag']
            variables = [c for c in variables if c != time_col]
        
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


    def OBSOLETE_read_all(self,node_id,col_name=None):
        assert type(node_id) is int,'storage::read_all(): node_id must be int'
        self.c.row_factory = sqlite3.Row
        if col_name is None:
            col_name = self._capability[node_id]['dbtag']
            #col_name = ['*']
        table_name = 'node_{:03d}'.format(node_id)

        cmd = 'SELECT {} FROM {}'.format(','.join(col_name),table_name)
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        tmp = [list(r) for r in zip(*tmp)]
        return dict(zip(col_name,tmp))

    # if nhour is specified, read the records in the last nhour hours
    # else if count is specified, read the last count records
    # "last" is determinted by time_col
    def OBSOLETE_read_latest(self,node_id,col_name=None,nhour=None,count=1,time_col=None):
        assert type(node_id) is int,'storage::read_latest(): node_id must be int'
        assert count >= 1

        if col_name is None:
            col_name = self._capability[node_id]['dbtag']
            #col_name = ['*']     # better?
        if time_col is None:
            time_col = 'ReceptionTime'
        table_name = 'node_{:03d}'.format(node_id)
        
        if nhour is not None:
            cmd = '''SELECT {} FROM {} WHERE 
                {} > DATETIME("now","-{} hours") ORDER BY {}'''.\
                format(','.join(col_name),table_name,time_col,nhour,time_col)
            self.c.execute(cmd)
            tmp = self.c.fetchall()
            tmp = [list(r) for r in zip(*tmp)]
            return dict(zip(col_name,tmp))
        else:
            #cmd = '''SELECT {} FROM {} WHERE Timestamp IN (SELECT max(Timestamp) FROM Samples) ORDER BY Timestamp'''.\
            #    format(','.join(col_name),'node_{:03d}'.format(node_id))
            #print cmd
            cmd = '''SELECT {} FROM (SELECT * FROM {} ORDER BY {} DESC LIMIT ?)
                ORDER BY {}'''.format(','.join(col_name),table_name,time_col,time_col)
            self.c.execute(cmd,(count,))    # tricky bas-. mind that trailing comma.
            tmp = self.c.fetchall()
            tmp = [list(r) for r in zip(*tmp)]
            return dict(zip(col_name,tmp))

    # time_col: specify the column used as time index.
    # Only some node report time of sampling Timestamp, but all nodes have ReceptionTime.
    def OBSOLETE_hourly_average(self,node_id,col_name=None,time_col=None):
        assert type(node_id) is int,'storage::hourly_average(): node_id must be int'
        if col_name is None:
            col_name = self._capability[node_id]['dbtag']
        if time_col is None:
            time_col = 'ReceptionTime'
        table_name = 'node_{:03d}'.format(node_id)
        tmp = ','.join(['avg({})']*len(col_name))
        tmp = tmp.format(*col_name)

        tmp = '{},{}'.format(time_col,tmp)
        cmd = '''SELECT {} FROM {} GROUP BY
            strftime("%Y%m%d%H",{})'''.format(tmp,table_name,time_col)
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        tmp = [list(r) for r in zip(*tmp)]
        #return tmp
        col_name.insert(0,time_col)
        return dict(zip(col_name,tmp))


if '__main__' == __name__:

    node_id = 4
    var = ['Pressure_BMP180']
    
    store = storage()

    print
    print 'read_latest()'
    tmp = store.read_latest(node_id)
    print tmp
    
    print
    print 'read_time_range()'
    tmp = store.read_time_range(node_id,time_col='Timestamp')
    print tmp
    print type(tmp[0])

    print
    print 'read max six entries (should have precedence over nhour)'
    tmp = store.read(node_id,nhour=10,count=6)
    print tmp

    print
    print 'hourly average of "{}" in the past 1 day, 3 hours'.format(var)
    tmp = store.read(node_id,variables=var,nhour=3,nday=1,avg='hourly')
    print tmp.keys()
    print len(tmp[var[0]])

    print
    print 'daily average of the past 14 days, all variables'
    tmp = store.read(node_id,nday=14,avg='daily')
    print tmp.keys()
    print len(tmp[var[0]])

    print
    print 'past 6 hours, all variables'
    tmp = store.read(node_id,nhour=6)
    print tmp.keys()
    print len(tmp[var[0]])

    # read everything
#    tmp = store.read(node_id)
#    print
#    print tmp.keys()
#    print len(tmp[var])

#    tmp = store.read_all(node_id)
#    print
#    print tmp.keys()
#    print len(tmp[var])
    
