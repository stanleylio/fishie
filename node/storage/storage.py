#!/usr/bin/python
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import sqlite3,re,sys
sys.path.append('..')
from ConfigParser import RawConfigParser,NoSectionError
from os.path import join,dirname
from parse_support import read_capability


def PRINT(s):
    #pass
    print(s)

# one table per node
# one column per variable

class storage(object):
    def __init__(self):
        try:
            self.conn = sqlite3.connect(join(dirname(__file__),'sensor_data.db'),\
                                        detect_types=sqlite3.PARSE_DECLTYPES |\
                                        sqlite3.PARSE_COLNAMES)
            self.c = self.conn.cursor()
            self.c.execute('PRAGMA journal_mode = WAL')

            def dict_factory(cursor,row):
                d = {}
                for idx,col in enumerate(cursor.description):
                    d[col[0]] = row[idx]
                return d
            #self.c.row_factory = dict_factory
            self.c.row_factory = sqlite3.Row

            self.nodes = read_capability()
            for node_id in self.nodes.keys():
                dbtag = self.nodes[node_id]['dbtag']
                dbtype = self.nodes[node_id]['dbtype']

                table_name = 'node_{:03d}'.format(node_id)
                schema = '({})'.format(','.join([' '.join(p) for p in zip(dbtag,dbtype)]))
                cmd = 'CREATE TABLE IF NOT EXISTS {} {}'.format(table_name,schema)
                self.c.execute(cmd)

                insertcmd = 'INSERT OR REPLACE INTO {} VALUES{}'.\
                         format(table_name,'({})'.format(','.join('?'*len(dbtype))))
                self.nodes[node_id]['insertcmd'] = insertcmd

        except NoSectionError as e:
            PRINT('storage: configuration file not found.')
            raise e

    # as long as the caller supply all the required values
    # ignore the extra ones, like Checksum or other
    # what is "required" for each node is defined in the configuration file, "dbtag"
    def write(self,node_id,readings):
        table_name = 'node_{:03d}'.format(node_id)
        dbtag = self.nodes[node_id]['dbtag']
        readings = [readings[v] for v in dbtag]
        cmd = 'INSERT OR REPLACE INTO {} ({}) VALUES({})'.\
              format(table_name,','.join(dbtag),','.join('?'*len(dbtag)))
        self.c.execute(cmd,readings)
        self.conn.commit()

    def read_all(self,node_id,col_name=None):
        assert type(node_id) is int,'storage::read_all(): node_id must be int'
        self.c.row_factory = sqlite3.Row
        if col_name is None:
            col_name = self.nodes[node_id]['dbtag']
        table_name = 'node_{:03d}'.format(node_id)

        cmd = 'SELECT {} FROM {}'.format(','.join(col_name),table_name)
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        tmp = [list(r) for r in zip(*tmp)]
        return dict(zip(col_name,tmp))
        

    # if nhour is specified, read the records in the last nhour hours
    # else if count is specified, read the last count records
    # "last" is determinted by time_col
    def read_latest(self,node_id,col_name=None,nhour=None,count=1,time_col=None):
        assert type(node_id) is int,'storage::read_latest(): node_id must be int'
        assert count >= 1

        if col_name is None:
            col_name = self.nodes[node_id]['dbtag']
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
    def hourly_average(self,node_id,col_name=None,time_col=None):
        assert type(node_id) is int,'storage::hourly_average(): node_id must be int'
        if col_name is None:
            col_name = self.nodes[node_id]['dbtag']
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
    store = storage()

    tmp = store.read_latest(4,count=2)
    print tmp
    
    #from datetime import datetime
    #store.write(1,(datetime.utcnow(),2,3,4))
    #print store.read_latest(1)

