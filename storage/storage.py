#!/usr/bin/python
#
# avg() and count() are nice though...
#
# Stanley Hou In Lio, hlio@hawaii.edu
# October, 2015
import sqlite3,time,traceback,logging
from os.path import join,dirname
from datetime import datetime,timedelta
from os.path import exists
import sys
sys.path.append('..')
from helper import ts2dt,dt2ts


def auto_time_col(store,node_id):
    time_col = 'Timestamp'
    if 'ReceptionTime' in store.get_list_of_columns(node_id):
        time_col = 'ReceptionTime'
    return time_col


# this one doesn't require database schema on instantiation
class storage_read_only(object):
    def __init__(self,dbfile=None,create_if_not_exists=False):  # wait, if it's read-only then it should already exist. TODO
        if dbfile is None:
            dbfile = join(dirname(__file__),'sensor_data.db')
            logging.warning('dbfile not specified. Default to ' + dbfile)
        if not create_if_not_exists and not exists(dbfile):
            raise IOError('{} does not exist.'.format(dbfile))
        self.conn = sqlite3.connect(dbfile,\
                                    detect_types=sqlite3.PARSE_DECLTYPES |\
                                    sqlite3.PARSE_COLNAMES)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.c.execute('PRAGMA journal_mode = WAL')

    @classmethod
    def id2table(self,node_id):
        return node_id.replace('-','_')

    # would be nice to be able to db.tables
    def get_list_of_tables(self):
        cursor = self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return sorted([t[0] for t in cursor.fetchall() if not t[0].startswith('sqlite_')])

    def get_list_of_columns(self,node_id):
        cursor = self.c.execute('SELECT * FROM {}'.format(self.id2table(node_id)))
        return [d[0] for d in cursor.description]

    def read_time_range(self,node_id,time_col,cols,begin,end=None):
        """Retrieve records in the given time period.
        If end is not specified, end = the moment this is called.
        """
        assert type(cols) is list,'cols must be a list of string'
        assert time_col in self.get_list_of_columns(node_id),\
               'no such time_col: {}'.format(time_col)

        if end is None:
            end = datetime.utcnow()
            if type(begin) is float:
                end = dt2ts(end)

        assert end > begin,'"begin" came after "end"? just swap the two'

        time_range = 'WHERE {time_col} BETWEEN "{begin}" AND "{end}"'.\
                     format(time_col=time_col,begin=begin,end=end)
        # SQLite doesn't have its own datetime type. Datetime ranking by string comparison
        # somehow seems hackish as it relies on comformity to the ISO8601 format.
        cmd = 'SELECT {} FROM {} {time_range} ORDER BY {time_col} DESC'.\
                format(','.join(cols),
                       self.id2table(node_id),
                       time_range=time_range,
                       time_col=time_col)
        return self._execute(cmd)

    def read_latest_non_null(self,node_id,time_col,var):
        """Retrieve the latest non-null record of var."""
        cols = [time_col,var]
        table = self.id2table(node_id)
        cmd = 'SELECT {} FROM {} WHERE {} IS NOT NULL ORDER BY {} DESC LIMIT 1;'.\
              format(','.join(cols),table,var,time_col)
        #print cmd
        try:
            self.c.execute(cmd)
            tmp = self.c.fetchall()
            if len(tmp) <= 0:
                return None
            return {v:tuple(r[v] for r in tmp)[0] for v in cols}
        except:
            return None

    # who is still using this? get rid of this. TODO
    def read_past_time_period(self,node_id,time_col,cols,timerange):
        """Retrieve records taken in the past timerange (a positive
        datetime.timedelta). (relative to the moment this is called)
        """
        end = datetime.utcnow()
        begin = end - timerange
        return self.read_time_range(node_id,time_col,cols,begin,end=end)

    def read_last_N(self,node_id,time_col,count=1,cols=None):
        """Retrieve the last N records."""
        assert cols is None or type(cols) is list,'storage::read_last_N(): cols, if not None, must be a list of string'

        if cols is None:
            cols = self.get_list_of_columns(node_id)
        else:
            if 'Timestamp' not in cols and 'ReceptionTime' not in cols:
                logging.warning('Sure you don''t want any timestamps?')

        cmd = 'SELECT {} FROM {} ORDER BY {} DESC LIMIT {}'.\
                format(','.join(cols),
                       self.id2table(node_id),
                       time_col,
                       count)
        return self._execute(cmd)

# I don't see the utility of this anymore. get rid of this. TODO
    def read_last_N_minutes(self,node_id,time_col,N,cols=None,nonnull=None):
        """Retrieve records within N minutes of the last record in the database.
        "Last N minutes" is relative to the latest record in the database (which could be
        days old in the case of sensor failure), not relative to the time this method is
        called.

        If nonnull is given, then the N minutes window is relative to the latest sample with
        the additional requirement that the said sample must not be Null (SQLite's Null is
        mapped to Python's None). For example, if the last non-null record of VAR was taken
        10 days ago, records up to N minutes prior to that sample are returned (which are
        all at least 10 days old, even though they are the "latest").
        """
        assert cols is None or type(cols) is list,'storage::read_last_N_minutes(): cols, if not None, must be a list of string'
        
        if cols is None:
            cols = self.get_list_of_columns(node_id)

        table = self.id2table(node_id)
        if nonnull is not None:
            cmd = '''SELECT {cols}
                     FROM {table} WHERE
                        DATETIME({time_col}) > 
                        DATETIME((SELECT {time_col} FROM {table} WHERE {nonnull} IS NOT NULL ORDER BY {time_col} DESC LIMIT 1),'-{N} minutes')
                        AND {nonnull} IS NOT NULL;
                    '''.format(cols=','.join(cols),time_col=time_col,table=table,N=N,nonnull=nonnull)
        else:
            cmd = "SELECT {cols} FROM {table} WHERE DATETIME({time_col}) > DATETIME((SELECT {time_col} FROM {table} ORDER BY {time_col} DESC LIMIT 1),'-{N} minutes');".\
                    format(cols=','.join(cols),time_col=time_col,table=table,N=N)
        return self._execute(cmd)

    def read_all(self,node_id,cols=None):
        """Retrieve all records as a dictionary."""
        if cols is None:    # or use * ?
            cols = self.get_list_of_columns(node_id)
        cmd = 'SELECT {cols} FROM {table}'.\
              format(cols=','.join(cols),table=self.id2table(node_id))
        return self._execute(cmd)

    def _execute(self,cmd):
        try:
            self.c.execute(cmd)
            tmp = self.c.fetchall()
            if len(tmp) <= 0:
                return None
            cols = [c[0] for c in self.c.description]
            return {v:tuple(r[v] for r in tmp) for v in cols}
        except:
            logging.error(traceback.format_exc())
            return None

    def OBSOLETE_execute(self,cmd):
        try:
            self.c.execute(cmd)
            tmp = self.c.fetchall()
            if len(tmp) <= 0:
                return None
            cols = [c[0] for c in self.c.description]
            return {v:tuple(r[v] for r in tmp) for v in cols}
        except:
            logging.error(traceback.format_exc())
            return None

    '''def OBSOLETE_execute(self,cmd):
        try:
            self.c.execute(cmd)
            tmp = self.c.fetchall()
            if len(tmp) <= 0:
                return None
            cols = [c[0] for c in self.c.description]
            return {v:tuple(r[v] for r in tmp) for v in cols}
        except:
            traceback.print_exc()
            return None'''

    def read_schema(self):
        return {t:self.get_list_of_columns(t) for t in self.get_list_of_tables()}

    def print_schema(self):
        tmp = self.read_schema()
        for table in tmp.keys():
            print table
            print '\t' + '\n\t'.join(tmp[table])


class storage(storage_read_only):
    def __init__(self,dbfile,schema=None):
        super(storage,self).__init__(dbfile=dbfile,create_if_not_exists=schema is not None)

        if schema is not None:
            for node,v in schema.iteritems():
                tmp = '({})'.format(','.join([' '.join(tmp) for tmp in schema[node]]))
                cmd = 'CREATE TABLE IF NOT EXISTS {} {}'.format(self.id2table(node),tmp)
                self.c.execute(cmd)

    # node is redundant. readings should contains readings['node']. TODO
    def write(self,readings):
        assert 'ReceptionTime' in readings.keys() or 'Timestamp' in readings.keys()
        node = readings['node']
        cols = self.get_list_of_columns(node)
        a = set(readings.keys())
        b = set(cols)
        # they are not mutrally exclusive. Check your math.
        if a - b:
            logging.warning('Warning: these are not defined in db and are ignored: ' + ','.join(a - b))
        if b - a:
            logging.warning('Warning: these fields defined in the db are not supplied: ' + ','.join(b - a))

        # filter out values that are not recorded by the database
        keys = list(set(readings.keys()) & set(self.get_list_of_columns(node)))
        vals = [readings[k] for k in keys]
        #cmd = 'INSERT OR REPLACE INTO {} ({}) VALUES ({})'.\
        cmd = 'INSERT INTO {} ({}) VALUES ({})'.\
              format(self.id2table(node),','.join(keys),','.join('?'*len(keys)))
        self.c.execute(cmd,vals)
        self.conn.commit()


if '__main__' == __name__:

    store = storage_read_only(dbfile='/home/nuc/data/base-003/storage/sensor_data.db')
    store.print_schema()
    #print store.read_last_N('node-003','ReceptionTime',2)

