import sqlite3
from ConfigParser import SafeConfigParser,NoSectionError
from os.path import join,dirname

# database interface
#
# Stanley Lio, hlio@usc.edu
# All Rights Reserved. February 2015

def PRINT(s):
    #pass
    print(s)

# by design, the first column is always (unique) Timestamps
# other than that, all other columns are specified by storage.ini
class storage(object):
    def __init__(self):
        try:
            parser = SafeConfigParser()
            parser.read(join(dirname(__file__),'../node_config.ini'))
            self.tag = parser.get('storage','tag').split(',')
            dbtype = parser.get('storage','dbtype').split(',')
            self.insertcmd = 'INSERT OR REPLACE INTO Samples VALUES{}'.\
                             format('({})'.format(','.join('?'*len(dbtype))))
            schema = '({})'.format(','.join([' '.join(p) for p in zip(self.tag,dbtype)]))
            # print schema
            
            self.conn = sqlite3.connect(join(dirname(__file__),'sensor_data.db'),\
                                        detect_types=sqlite3.PARSE_DECLTYPES |\
                                        sqlite3.PARSE_COLNAMES)
            self.c = self.conn.cursor()
            # important, allow simultaneous read/write
            # https://www.sqlite.org/wal.html
            self.c.execute('PRAGMA journal_mode = WAL')
            #self.c.execute('''CREATE TABLE IF NOT EXISTS Samples
                #(Timestamp TIMESTAMP UNIQUE,
                #Temp_BMP180 REAL,
                #Pressure_BMP180 REAL,
                #Temp_HTU21D REAL,
                #Humidity_HTU21D REAL)''')
            self.c.execute('CREATE TABLE IF NOT EXISTS Samples ' + schema)
            
        except NoSectionError as e:
            PRINT('storage: configuration file not found.')
            raise e

    def write(self,R):
        if type(R) is tuple:
            R = [R]
        for r in R:
            #self.c.execute('INSERT OR IGNORE INTO Samples VALUES(?,?,?,?,?)',r)
            #self.c.execute('INSERT OR REPLACE INTO Samples VALUES(?,?,?,?,?)',r)
            self.c.execute(self.insertcmd,r)
            self.conn.commit()

    # TODO: sql injection?
    # read one column as a list
    # not that useful on a live database
    #def read(self,col_name):
    #    self.c.row_factory = sqlite3.Row
    #    # hum... sql injection...?
    #    self.c.execute('SELECT {} FROM Samples ORDER BY Timestamp'.format(col_name))
    #    rows = self.c.fetchall()
    #    return [v[0] for v in rows]

    # sql injection?
    # read multiple columns as list of lists
    def read_all(self,col_name=None):
        self.c.row_factory = sqlite3.Row
        if col_name is None:
            col_name = self.tag
        
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
            col_name = self.tag
            
        if nhour is not None:
            cmd = '''SELECT {} FROM Samples WHERE 
                Timestamp > DATETIME("now","-{} hours") ORDER BY Timestamp'''.\
                format(','.join(col_name),nhour)
            self.c.execute(cmd)
            tmp = self.c.fetchall()
            tmp = [list(r) for r in zip(*tmp)]
            return tmp
        elif 1 == count:
            # if it's just the last entry...
            # just an sql exercise, not for efficiency consideration
            count = 1
            cmd = '''SELECT {} FROM Samples WHERE Timestamp IN (SELECT max(Timestamp)
                FROM Samples) ORDER BY Timestamp'''.format(','.join(col_name))
            self.c.execute(cmd)
            tmp = self.c.fetchone()
            tmp = [v for v in tmp]
            return tmp
        else:
            cmd = '''SELECT {} FROM (SELECT * FROM Samples ORDER BY Timestamp DESC LIMIT ?)
                ORDER BY Timestamp'''.format(','.join(col_name))
            self.c.execute(cmd,(count,))    # tricky bas-. mind that trailing comma.
            tmp = self.c.fetchall()
            tmp = [list(r) for r in zip(*tmp)]
            return tmp

    # first column is always Timestamp - don't include that in col_name
    # abstraction leak - a "storage" shouldn't be concerned with queries like this
    def hourly_average(self,col_name=None):
        if col_name is None:
            col_name = self.tag[1:]
        tmp = ','.join(['avg({})']*len(col_name))
        tmp = tmp.format(*col_name)
        cmd = '''SELECT Timestamp,{} FROM Samples GROUP BY
            strftime("%Y%m%d%H",Timestamp)'''.format(tmp)
        self.c.execute(cmd)
        tmp = self.c.fetchall()
        return [list(r) for r in zip(*tmp)]


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
    
