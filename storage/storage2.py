# compared to storage.py: this uses MySQL instead of SQLite
#
# Stanley H.I. Lio
# hlio@hawaii.edu
# All Rights Reserved. 2017
import time,sys,logging
from os.path import expanduser
sys.path.append(expanduser('~'))
import MySQLdb  # careful about stale read - sqlalchemy seems to handle this automatically; MySQLdb doesn't.
from datetime import datetime,timedelta


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def auto_time_col(columns):
    for time_col in ['ReceptionTime','Timestamp','ts']:
        if time_col in columns:
            return time_col
    assert False

# 'dbtag' is mandatory; everything else is optional.
# 'dbtype' defaults to DOUBLE
def create_table(conf,table,dbname='uhcm',user='root',password=None,host='localhost',noreceptiontime=False):
    if password is None:
        #password = open(expanduser('~/mysql_cred')).read().strip()
        from cred import cred
        passwd = cred['mysql']
    if not noreceptiontime:
        conf.insert(0,{'dbtag':'ReceptionTime','dbtype':'DOUBLE PRIMARY KEY'})
    conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=dbname)
    cur = conn.cursor()

    tmp = ','.join([' '.join(tmp) for tmp in [(column['dbtag'],column.get('dbtype','DOUBLE')) for column in conf]])
    cmd = 'CREATE TABLE IF NOT EXISTS {}.`{}` ({})'.format(dbname,table,tmp)
    logger.debug(cmd)
    cur.execute(cmd)


class storage():
    def __init__(self,dbname='uhcm',user='root',passwd=None,host='localhost'):
        if passwd is None:
            #passwd = open(expanduser('~/mysql_cred')).read().strip()
            from cred import cred
            passwd = cred['mysql']
        self._dbname = dbname
        self._schema_cache = {}     # need to restart log2mysql every time new fields are added. annoying.

        #print host,user,passwd,dbname
        self._conn = MySQLdb.connect(host=host,
                                     user=user,
                                     passwd=passwd,
                                     db=dbname)
        self._cur = self._conn.cursor()

    def get_list_of_tables(self):
        self._cur.execute('SHOW TABLES;')
        return [tmp[0] for tmp in self._cur.fetchall()]

    def get_list_of_columns(self,table):
        if table not in self._schema_cache:
            self._cur.execute('SELECT * FROM {}.`{}` LIMIT 1;'.format(self._dbname,table))
            self._schema_cache[table] = [tmp[0] for tmp in self._cur.description]
        return self._schema_cache[table]
    
    def insert(self,table,sample,autocommit=True):
        # strip the keys not defined in the db - SQLite didn't seem to care. MySQL does.
        sample = {k:sample[k] for k in self.get_list_of_columns(table) if k in sample}
        #cur = self._conn.cursor()
        #sample = [(k,v) for k,v in sample.iteritems()]
        #cols,vals = zip(*sample)
        cols,vals = zip(*sample.items())
        cmd = 'INSERT IGNORE INTO {}.`{table}` ({cols}) VALUES ({vals})'.\
              format(self._dbname,
                     table=table,
                     cols=','.join(cols),
                     vals=','.join(['%s']*len(cols)))
        #print(cmd)
        self._cur.execute(cmd,vals)
        if autocommit:
            self._conn.commit()

    def read_time_range(self,table,time_col,cols,begin,end):
        """Retrieve records in the given time period.
        If end is not specified, end = the moment this is called.
        Would be nice to auto-convert begin and end to suit the type of column time_col
        but that would mean doing a query just to find out the type... not worth it.
        """
        assert type(cols) is list,'cols must be a list of string'
        assert time_col in self.get_list_of_columns(table),'no such time_col: {}'.format(time_col)
        assert type(end) in [float,int]
        if end is None:
            end = time.time()

        assert type(end) in [float,int] and type(begin) in [float,int]
        # also require type(end) == type(begin) == type(stuff in column time_col)

        #cmd = 'SELECT {} FROM {}.`{}` {time_range} ORDER BY {time_col} DESC'.\
        cmd = 'SELECT {} FROM {}.`{}`'.\
                format(','.join(cols),
                       self._dbname,
                       table)
        time_range = ' WHERE {time_col} BETWEEN "{begin}" AND "{end}"'.\
                     format(time_col=time_col,begin=begin,end=end)
        cmd = cmd + time_range
        #print(cmd)
        self._cur.execute(cmd)
        r = self._cur.fetchall()
        self._conn.commit() # see: stale read
        if len(r):
            r = zip(*r)
            # {a:[],b:[]} vs. [[a0,b0],[a1,b1],[a2,b2]...]
            # this is the former, but the latter is more efficient.
            # once the API is public, it is set in stone. lesson learned.
            return {c:r[k] for k,c in enumerate(cols)}
        else:
            return {c:[] for k,c in enumerate(cols)}

    def read_time_range2(self,table,time_col,cols,begin,end):
        try:
            cmd = 'SELECT {} FROM {}.`{}`'.\
                    format(','.join(cols),
                           self._dbname,
                           table)
            time_range = ' WHERE {time_col} BETWEEN "{begin}" AND "{end}"'.\
                         format(time_col=time_col,begin=begin,end=end)
            cmd += time_range
            self._cur.execute(cmd)
            self._conn.commit()
            return self._cur.fetchall()
        except MySQLdb.OperationalError:
            logger.exception('read_time_range2() error')
            return []

    def read_last_N_minutes(self,table,time_col,N,nonnull):
        """get the latest N-minute worth of readings of the variable 'nonnull' where its readings were not NULL"""

        if nonnull not in self.get_list_of_columns(table):
            return {time_col:[],nonnull:[]}
        
        cmd = '''SELECT {time_col},{nonnull} FROM `{table}` WHERE
                {time_col} >= (SELECT MAX({time_col}) - {N} FROM (SELECT {time_col},{nonnull} FROM `{table}` WHERE {nonnull} IS NOT NULL) AS T)
                AND
                {nonnull} IS NOT NULL;'''.\
                format(time_col=time_col,table=table,N=60*N,nonnull=nonnull)
        self._cur.execute(cmd)
        r = self._cur.fetchall()
        self._conn.commit()
        if len(r):
            r = zip(*r)
            return {time_col:list(r[0]),nonnull:list(r[1])}
        else:
            return {time_col:[],nonnull:[]}

    '''def read_latest_non_null(self,table,time_col,var):
        """Retrieve the latest non-null record of var."""
        r = self.read_last_N_minutes(table,time_col,1,var)
        if len(r[time_col]):
            L = zip(r[time_col],r[var])
            L.sort(key=lambda x: x[0])
            return {time_col:L[-1][0],var:L[-1][1]}
        else:
            return {time_col:[],var:[]}'''

    def read_latest_non_null(self,table,time_col,var):
        """Retrieve the latest row where var is not null."""
        cmd = '''SELECT * FROM `{table}` WHERE {var} IS NOT NULL ORDER BY {time_col} DESC LIMIT 1;'''.\
              format(time_col=time_col,var=var,table=table)
        self._cur.execute(cmd)
        r = self._cur.fetchall()
        self._conn.commit()
        if len(r):
            cols = self.get_list_of_columns(table)
            return dict(zip(cols,r[0]))
            #return {time_col:r[0][0],var:r[0][1]}
        else:
            return {time_col:None,var:None}

    def commit(self):
        self._conn.commit()


if '__main__' == __name__:
    import time
    s = storage()
    #print(s.read_time_range('node-010','ReceptionTime',['ReceptionTime','d2w'],dt2ts()-3600,dt2ts()))
    #print(s.read_last_N_minutes('node-011','ReceptionTime',5,nonnull='d2w'))
    print(s.read_time_range2('node-022','ReceptionTime',['ReceptionTime,PH_EXT'],time.time()-600,time.time()))
