"""A poorly-made ORM training wheel is what this is. Should go track
down all the callers and get rid of this script.

Stanley H.I. Lio
"""
import time, sys, logging, MySQLdb
from os.path import expanduser
sys.path.append(expanduser('~'))


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# 'dbtag' is mandatory; everything else is optional.
# 'dbtype' defaults to DOUBLE
def create_table(conf, table, *, dbname='uhcm', user='s', password='', host='localhost', noreceptiontime=False):
    if not noreceptiontime:
        conf.insert(0, {'dbtag':'ReceptionTime', 'dbtype':'DOUBLE PRIMARY KEY'})
    conn = MySQLdb.connect(host=host, user=user, passwd=password, db=dbname)
    with conn:
        cur = conn.cursor()
        tmp = ','.join([' '.join(tmp) for tmp in [(column['dbtag'], column.get('dbtype', 'DOUBLE')) for column in conf]])
        cmd = """CREATE TABLE IF NOT EXISTS uhcm.`{}` ({})""".format(table, tmp)
        cur.execute(cmd)


class Storage:
    def __init__(self, *, user='s', passwd='', host='localhost'):
        self._conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db='uhcm')
        self._cur = self._conn.cursor()

    def has_such_node(self, nodeid):
        self._cur.execute("""SELECT * FROM uhcm.devices WHERE nodeid=%s""", (nodeid, ))
        return self._cur.fetchone() is not None

# who's still using these?
    def get_list_of_tables(self):
        self._cur.execute("""SELECT nodeid FROM uhcm.devices ORDER BY nodeid""")
        return list(zip(*self._cur.fetchall()))[0]

    def get_list_of_columns(self, table):
        self._cur.execute("""SELECT name FROM uhcm.variables
                             WHERE nodeid=%s""", (table, ))
        return list(zip(*self._cur.fetchall()))[0]
    
    def insert(self, table, sample):
        if not self.has_such_node(table):
            logger.warning('{} not defined in db. ignore'.format(table))
            return
        # Strip the fields not defined in the db - SQLite doesn't seem
        # to care; MySQLdb does.
        known_cols = self.get_list_of_columns(table)
        cols = set(known_cols) & set(sample.keys())
        vals = [sample[c] for c in cols]
        cmd = 'INSERT IGNORE INTO uhcm.`{table}` ({cols}) VALUES ({vals})'.\
              format(table=table,
                     cols=','.join(cols),
                     vals=','.join(['%s']*len(cols)))
        self._cur.execute(cmd, vals)
        self._conn.commit()

    def read_time_range(self, table, time_col, cols, begin, end):
        """Retrieve records in the given time period. Return a dict with
        cols as keys and lists of readings as values.

        If end is not specified, end = the moment this is called. Would
        be nice to auto-convert begin and end to suit the type of column
        time_col but that would mean doing a query just to find out the
        type... not worth it.
        """
        assert type(cols) is list, 'cols must be a list of string'
        assert type(end) in [float, int] and type(begin) in [float, int]
        assert time_col in self.get_list_of_columns(table), 'no such time_col: {}'.format(time_col)

        r = self.read_time_range2(table, time_col, cols, begin, end)
        if len(r):
            return dict(zip(cols, zip(*r)))
        else:
            return {c:[] for c in cols}

    def read_time_range2(self, table, time_col, cols, begin, end):
        """I don't know why I didn't start with this version. The caller
        provided cols so they know what the variables are and in what
        order. There is no point putting data result in a dictionary.
        """
        try:
            cmd = """SELECT {} FROM uhcm.`{}`
                     WHERE {} BETWEEN %s AND %s""".format(','.join(cols), table, time_col)
            self._cur.execute(cmd, (begin, end, ))
            return list(self._cur.fetchall())
        except MySQLdb.OperationalError:
            logger.exception('{} {} {} {} {}'.format(table, time_col, cols, begin, end))
        return []

# who's still using these?
    def read_last_N_minutes(self, table, time_col, N, nonnull):
        """Get the latest N-minute worth of readings of the variable
        'nonnull' where its readings were not NULL
        """

        if nonnull not in self.get_list_of_columns(table):
            return {time_col:[], nonnull:[]}
        
        cmd = '''SELECT {time_col},{nonnull} FROM `{table}` WHERE
                {time_col} >= (SELECT MAX({time_col}) - {N} FROM (SELECT {time_col},{nonnull} FROM `{table}` WHERE {nonnull} IS NOT NULL) AS T)
                AND
                {nonnull} IS NOT NULL;'''.\
                format(time_col=time_col, table=table, N=60*N, nonnull=nonnull)
        self._cur.execute(cmd)
        r = self._cur.fetchall()
        self._conn.commit()
        if len(r):
            r = list(zip(*r))
            return {time_col:list(r[0]), nonnull:list(r[1])}
        else:
            return {time_col:[], nonnull:[]}

# who's still using these?
    def read_latest_non_null(self, table, time_col, var):
        """Retrieve the latest row where var is not null."""
        
        cmd = 'SELECT * FROM `{table}` WHERE {var} IS NOT NULL ORDER BY {time_col} DESC LIMIT 1;'.\
              format(time_col=time_col, var=var, table=table)
        self._cur.execute(cmd)
        r = self._cur.fetchall()
        self._conn.commit()
        if len(r):
            cols = self.get_list_of_columns(table)
            return dict(zip(cols, r[0]))
        else:
            return {time_col:None, var:None}

    def commit(self):
        self._conn.commit()


if '__main__' == __name__:
    import time
    s = Storage()
    #print(s.read_time_range('node-010','ReceptionTime',['ReceptionTime','d2w'],dt2ts()-3600,dt2ts()))
    #print(s.read_last_N_minutes('node-011','ReceptionTime',5,nonnull='d2w'))
    print(s.read_time_range2('node-097', 'ReceptionTime', ['ReceptionTime', 'd2w'], time.time()-600, time.time()))
