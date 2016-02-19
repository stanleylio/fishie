#!/usr/bin/python
#
# avg() and count() are nice though...
#
# Stanley Hou In Lio, hlio@hawaii.edu
# October, 2015
import sqlite3,time,traceback
from os.path import join,dirname
from datetime import datetime,timedelta
from os.path import exists


def PRINT(s):
    #pass
    print(s)

def auto_time_col(store,node_id):
    time_col = 'Timestamp'
    if 'ReceptionTime' in store.get_list_of_columns(node_id):
        time_col = 'ReceptionTime'
    return time_col

def id2table(node_id):
    return node_id.replace('-','_')


# this one doesn't require database schema on instantiation
class storage_read_only(object):
    def __init__(self,dbfile=None,create_if_not_exists=False):
        if dbfile is None:
            dbfile = join(dirname(__file__),'sensor_data.db')
            PRINT('dbfile not specified. Default to ' + dbfile)
        if not create_if_not_exists and not exists(dbfile):
            raise IOError('{} does not exist. Set create_if_not_exists=True to override.'.format(dbfile))
        self.conn = sqlite3.connect(dbfile,\
                                    detect_types=sqlite3.PARSE_DECLTYPES |\
                                    sqlite3.PARSE_COLNAMES)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.c.execute('PRAGMA journal_mode = WAL')

    def get_list_of_tables(self):
        cursor = self.c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return sorted([t[0] for t in cursor.fetchall() if not t[0].startswith('sqlite_')])

    def get_list_of_columns(self,node_id):
        cursor = self.c.execute('SELECT * FROM {}'.format(id2table(node_id)))
        return [d[0] for d in cursor.description]

    def read_time_range(self,node_id,time_col,cols,begin,end=None):
        """Retrieve records in the given time period.
        If end is not specified, end = the moment this is called.
        """
        assert type(cols) is list,'cols must be a list of string'
        assert time_col in self.get_list_of_columns(node_id),\
               'no such time_col: {}'.format(time_col)

        if end is None:
            end = datetime.now()

        assert end > begin,'"begin" came after "end"? just swap the two'

        time_range = 'WHERE {time_col} BETWEEN "{begin}" AND "{end}"'.\
                     format(time_col=time_col,begin=begin,end=end)
        # SQLite doesn't have its own datetime type. Datetime ranking by string comparison
        # somehow seems hackish as it relies on comformity to the ISO8601 format.
        cmd = 'SELECT {} FROM {} {time_range} ORDER BY {time_col} DESC'.\
                format(','.join(cols),
                       id2table(node_id),
                       time_range=time_range,
                       time_col=time_col)
        return self._execute(cmd)

    def read_latest_non_null(self,node_id,time_col,var):
        """Retrieve the latest non-null record of var."""
        cols = [time_col,var]
        table = id2table(node_id)
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

    def read_past_time_period(self,node_id,time_col,cols,timerange):
        """Retrieve records in taken in the past timerange (a positive
        datetime.timedelta). (relative to the moment this is called)
        """
        end = datetime.now()
        begin = end - timerange
        return self.read_time_range(node_id,time_col,cols,begin,end=end)

    def read_last_N(self,node_id,time_col,count=1,cols=None):
        """Retrieve the last N records."""
        assert cols is None or type(cols) is list,'storage::read_last_N(): cols, if not None, must be a list of string'

        if cols is None:
            cols = self.get_list_of_columns(node_id)
        else:
            if 'Timestamp' not in cols and 'ReceptionTime' not in cols:
                print('Sure you don''t want any timestamps?')

        cmd = 'SELECT {} FROM {} ORDER BY {} DESC LIMIT {}'.\
                format(','.join(cols),
                       id2table(node_id),
                       time_col,
                       count)
        return self._execute(cmd)

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

        table = id2table(node_id)
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
        if cols is None:
            cols = self.get_list_of_columns(node_id)
        cmd = 'SELECT {cols} FROM {table}'.\
              format(cols=','.join(cols),table=id2table(node_id))
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
            return None

    def read_schema(self):
        return {t:self.get_list_of_columns(t) for t in self.get_list_of_tables()}

    def print_schema(self):
        tmp = self.read_schema()
        for table in tmp.keys():
            print table
            print '\t' + '\n\t'.join(tmp[table])


class storage(storage_read_only):
    def __init__(self,schema,dbfile=None,create_if_not_exists=True):
        super(storage,self).__init__(dbfile=dbfile,create_if_not_exists=create_if_not_exists)
        # TODO: either supply schema or dbfile.
        #   if only schema is supplied, create if not exist.
        #   if only dbfile is supplied, raise if not exists(dbfile)
        #   reject if both are supplied
        self._schema = schema   # TODO: and get rid of this. write() should not need it.
        for node_id,v in self._schema.iteritems():
            tmp = '({})'.format(','.join([' '.join(p) for p in zip(v['tag'],v['type'])]))
            cmd = 'CREATE TABLE IF NOT EXISTS {} {}'.format(id2table(node_id),tmp)
            self.c.execute(cmd)
    
    # Three cases:
    #   More keys than columns
    #       Filter out keys not in the database
    #   The set of keys matches the set of columns
    #   More columns than keys
    #       Handled by the database - missing fields are replaced by NULLs
    #
    # ... what about both sets have non-empty insection but both have exclusive elements?
    def write(self,node_id,readings):
        assert self._schema is not None
        assert 'ReceptionTime' in readings.keys() or 'Timestamp' in readings.keys()

        #cols = self.get_list_of_columns(node_id)
        
        if len(readings.keys()) > len(self._schema[node_id]['tag']):
        #if len(readings.keys()) > len(cols):
            PRINT('storage.py::write(): Warning: these are not defined in db and are ignored:')
            PRINT(','.join([t for t in readings.keys() if t not in self._schema[node_id]['tag']]))
            #PRINT(','.join([t for t in readings.keys() if t not in cols]))

        if len(readings.keys()) < len(self._schema[node_id]['tag']):
        #if len(readings.keys()) < len(cols):
            PRINT('storage.py::write(): Warning: the following are defined in the db but are not provided:')
            PRINT(','.join([t for t in self._schema[node_id]['tag'] if t not in readings.keys()]))
            #PRINT(','.join([t for t in cols if t not in readings.keys()]))

        # filter out readings that are not recorded by the database
        keys = [k for k in readings.keys() if k in self._schema[node_id]['tag']]
        #keys = [k for k in readings.keys() if k in self.get_list_of_columns(node_id)]
        vals = [readings[k] for k in keys]
        cmd = 'INSERT OR REPLACE INTO {} ({}) VALUES ({})'.\
              format(id2table(node_id),','.join(keys),','.join('?'*len(keys)))

        self.c.execute(cmd,vals)
        self.conn.commit()

    # TODO: should replace write() with this.
    def write2(self,node,readings):
        assert 'ReceptionTime' in readings.keys() or 'Timestamp' in readings.keys()

        cols = self.get_list_of_columns(node)
        if len(readings.keys()) > len(cols):
            PRINT('Warning: these are not defined in db and are ignored:')
            PRINT(','.join([t for t in readings.keys() if t not in cols]))
        elif len(readings.keys()) < len(cols):
            PRINT('Warning: these are defined in the db but are not given:')
            PRINT(','.join([t for t in cols if t not in readings.keys()]))

        # filter out readings that are not recorded by the database
        keys = [k for k in readings.keys() if k in self.get_list_of_columns(node)]
        vals = [readings[k] for k in keys]
        cmd = 'INSERT OR REPLACE INTO {} ({}) VALUES ({})'.\
              format(id2table(node),','.join(keys),','.join('?'*len(keys)))

        self.c.execute(cmd,vals)
        self.conn.commit()


if '__main__' == __name__:

    store = storage_read_only(dbfile='/home/nuc/data/base-003/storage/sensor_data.db')
    store.print_schema()
    #print store.read_last_N('node-003','ReceptionTime',2)

