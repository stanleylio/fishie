# database interface
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

import sqlite3,re,sys
sys.path.append('..')
from ConfigParser import SafeConfigParser,NoSectionError
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
            parser = SafeConfigParser()
            parser.read(join(dirname(__file__),'../node_config.ini'))
            self.dbtag = parser.get('storage','dbtag').split(',')
            dbtype = parser.get('storage','dbtype').split(',')
            self.insertcmd = 'INSERT OR REPLACE INTO Samples VALUES{}'.\
                             format('({})'.format(','.join('?'*len(dbtype))))
            schema = '({})'.format(','.join([' '.join(p) for p in zip(self.dbtag,dbtype)]))
            # print schema
            
            self.conn = sqlite3.connect(join(dirname(__file__),'sensor_data.db'),\
                                        detect_types=sqlite3.PARSE_DECLTYPES |\
                                        sqlite3.PARSE_COLNAMES)
            self.c = self.conn.cursor()
            # important, allow simultaneous read/write
            # https://www.sqlite.org/wal.html
            self.c.execute('PRAGMA journal_mode = WAL')
            self.c.execute('CREATE TABLE IF NOT EXISTS Samples ' + schema)
            
        except NoSectionError as e:
            PRINT('storage: configuration file not found.')
            raise e

    def write(self,node_id,readings):
        table_name = 'node_{:03d}'.format(node_id)
        
self.c.execute(self.insertcmd,r)
self.conn.commit()

    # sql injection?
    # read multiple columns as list of lists
    def read_all(self,col_name=None):
        self.c.row_factory = sqlite3.Row
        if col_name is None:
            col_name = self.dbtag
        
        # so this won't work.
        #self.c.execute('SELECT ?,? FROM Samples LIMIT 4',('Timestamp','Temp_BMP180',))
        # OK, looks like column and table names cannot be parametrized. but sql injection???
        cmd = 'SELECT {} FROM Samples ORDER BY Timestamp'.format(','.join(col_name))
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        # I can't change the API design everything matplotlib/sqlite3/whatever comes around
        # and demand to use its own format can I.
        return [list(r) for r in zip(*tmp)]

    def read_latest(self,col_name=None,nhour=None,count=1):
        self.c.row_factory = sqlite3.Row
        if col_name is None:
            col_name = self.dbtag
            
        if nhour is not None:
            cmd = '''SELECT {} FROM Samples WHERE 
                Timestamp > DATETIME("now","-{} hours") ORDER BY Timestamp'''.\
                format(','.join(col_name),nhour)
            self.c.execute(cmd)
            tmp = self.c.fetchall()
            tmp = [list(r) for r in zip(*tmp)]
            return tmp
        else:
            cmd = '''SELECT {} FROM (SELECT * FROM Samples ORDER BY Timestamp DESC LIMIT ?)
                ORDER BY Timestamp'''.format(','.join(col_name))
            self.c.execute(cmd,(count,))    # tricky bas-. mind that trailing comma.
            tmp = self.c.fetchall()
            tmp = [list(r) for r in zip(*tmp)]
            return dict(zip(col_name,tmp))

    # first column is always Timestamp - don't include that in col_name
    # abstraction leak - a "storage" shouldn't be concerned with queries like this
    def hourly_average(self,col_name=None,time_col='Timestamp'):
        if col_name is None:
            col_name = self.dbtag[1:]
        tmp = ','.join(['avg({})']*len(col_name))
        tmp = tmp.format(*col_name)
        cmd = '''SELECT {time_col},{} FROM Samples GROUP BY
            strftime("%Y%m%d%H",{time_col})'''.format(tmp,time_col=time_col)
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        tmp = [list(r) for r in zip(*tmp)]
        col_name.insert(0,time_col)
        return dict(zip(col_name,tmp))


if '__main__' == __name__:
    store = storage()

    col_name = ['Timestamp','Temp_BMP180','Pressure_BMP180','Temp_HTU21D','Humidity_HTU21D']
    #tmp = store.read_all(col_name)
    #print tmp
    #print len(tmp)
    #print len(tmp[0])
    
    #tmp = store.read_latest(col_name,count=10)
    #print type(tmp)
    #print len(tmp)
    #for r in zip(*tmp):
        #print r

    #tmp = store.read_latest(nhour=1)
    #tmp = zip(*tmp)
    #print len(tmp)
    #for r in tmp:
        #print r

    tmp = store.hourly_average()
    for r in zip(*tmp):
        print r
    
