import time,sys
from os.path import expanduser
sys.path.append(expanduser('~/node'))
import MySQLdb
from datetime import datetime,timedelta
from helper import dt2ts


def auto_time_col(columns):
    for time_col in ['ReceptionTime','Timestamp','ts']:
        if time_col in columns:
            return time_col
    assert False

def id2table(node_id):
    return node_id.replace('-','_')


class storage_read_only():
    def __init__(self,dbname='uhcm'):
        self._dbname = dbname
        self._conn = MySQLdb.connect(host='localhost',
                                     user='root',
                                     passwd=open(expanduser('~/mysql_cred')).read().strip(),
                                     db=dbname)
        self._cur = self._conn.cursor()

    def get_list_of_tables(self):
        self._cur.execute('SHOW TABLES;')
        return [tmp[0] for tmp in self._cur.fetchall()]

    def get_list_of_columns(self,table):
        self._cur.execute('SELECT * FROM {}.`{}` LIMIT 2;'.format(self._dbname,table))
        return [tmp[0] for tmp in self._cur.description]
    
    def read_time_range(self,node_id,time_col,cols,begin,end=None):
        """Retrieve records in the given time period.
        If end is not specified, end = the moment this is called.
        Would be nice to auto-convert begin and end to suit the type of column time_col
        but that would mean doing a query just to find out the type... not worth it.
        """
        assert type(cols) is list,'cols must be a list of string'
        table = id2table(node_id)
        assert time_col in self.get_list_of_columns(table),'no such time_col: {}'.format(time_col)

        if end is None:
            end = datetime.utcnow()
            if type(begin) is not datetime:
                end = dt2ts(end)

        assert type(end) == type(begin)
        assert end > begin,'"begin" came after "end"? just swap the two'
        # also require type(end) == type(begin) == type(stuff in column time_col)

        time_range = 'WHERE {time_col} BETWEEN "{begin}" AND "{end}"'.\
                     format(time_col=time_col,begin=begin,end=end)
        cmd = 'SELECT {} FROM {} {time_range} ORDER BY {time_col} DESC'.\
                format(','.join(cols),
                       table,
                       time_range=time_range,
                       time_col=time_col)
        self._cur.execute(cmd)
        r = self._cur.fetchall()
        r = zip(*r)
        return {c:r[k] for k,c in enumerate(cols)}

    def read_last_N_minutes(self,node_id,time_col,N,nonnull):
        table = id2table(node_id)

        cmd = '''SELECT {time_col},{nonnull} FROM {table} WHERE
                    {time_col} >= (SELECT MAX({time_col}) - {N} FROM (SELECT {time_col},{nonnull} FROM {table} WHERE {nonnull} IS NOT NULL) AS T)
                 AND
                    {nonnull} IS NOT NULL;'''.\
                format(time_col=time_col,table=table,N=60*N,nonnull=nonnull)
        self._cur.execute(cmd)
        r = self._cur.fetchall()
        r = zip(*r)
        return {time_col:list(r[0]),nonnull:list(r[1])}

    def read_latest_non_null(self,node_id,time_col,var):
        """Retrieve the latest non-null record of var."""
        r = self.read_last_N_minutes(node_id,time_col,1,var)
        L = zip(r[time_col],r[var])
        L.sort(key=lambda x: x[0])
        return {time_col:L[-1][0],var:L[-1][1]}


if '__main__' == __name__:
    s = storage_read_only()
    print s.read_time_range('node-010','ReceptionTime',['ReceptionTime','d2w'],dt2ts()-3600)
    print s.read_last_N_minutes('node-011','ReceptionTime',5,nonnull='d2w')
