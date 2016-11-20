import time,sys
from os.path import expanduser
sys.path.append(expanduser('~/node'))
from sqlalchemy import create_engine
from sqlalchemy import inspect
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
    def __init__(self):
        dbname = 'uhcm'
        self.engine = create_engine('mysql+mysqldb://root:' + open(expanduser('~/mysql_cred')).read() + '@localhost/' + dbname)
        self.insp = inspect(self.engine)

    def get_list_of_tables(self):
        return self.insp.get_table_names()

    def get_list_of_columns(self,table):
        return [c['name'] for c in self.insp.get_columns(table)]
    
    def read_time_range(self,node_id,time_col,cols,begin,end=None):
        """Retrieve records in the given time period.
        If end is not specified, end = the moment this is called.
        """
        assert type(cols) is list,'cols must be a list of string'
        table = id2table(node_id)
        assert time_col in self.get_list_of_columns(table),'no such time_col: {}'.format(time_col)

        if end is None:
            end = datetime.utcnow()
            if type(begin) is not datetime:
                end = dt2ts(end)

        assert end > begin,'"begin" came after "end"? just swap the two'

        time_range = 'WHERE {time_col} BETWEEN "{begin}" AND "{end}"'.\
                     format(time_col=time_col,begin=begin,end=end)
        cmd = 'SELECT {} FROM {} {time_range} ORDER BY {time_col} DESC'.\
                format(','.join(cols),
                       table,
                       time_range=time_range,
                       time_col=time_col)
        result = list(self.engine.execute(cmd))
        return {c:tuple(row[c] for row in result) for c in cols}

    def read_last_N_minutes(self,node_id,time_col,N,cols,nonnull=None):
        assert type(cols) is list,'storage::read_last_N_minutes(): cols must be a list of string'
        return self.read_time_range(node_id,time_col,cols,dt2ts() - timedelta(minutes=N).total_seconds())


if '__main__' == __name__:
    s = storage_read_only()
    print s.read_time_range('node-010','ReceptionTime',['ReceptionTime','d2w'],dt2ts()-3600)
    exit()


    

    for table in insp.get_table_names():
        print table
        #for c in insp.get_columns(table):
            #print '\t', c['name']
            #print session.query(c).first()
            #print [prop for prop in class_mapper(dbstuff.BME280_Sample).iterate_properties]
        columns = [c['name'] for c in insp.get_columns(table)]
        time_col = auto_time_col(columns)
        #print
        for r in engine.execute('SELECT * FROM ' + table + ' ORDER BY ' + time_col + ' DESC LIMIT 1;'):
            print '\t', timedelta(seconds=dt2ts() - r[time_col]), ' ago' #, ','.join([str(v) for v in r])
            #for k in r.keys():
                #if k not in ['ReceptionTime']:
                    #print '\t{}\t{}'.format(k,r[k])
