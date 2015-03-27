import sqlite3
from datetime import datetime


conn = sqlite3.connect('haha.db',\
                            detect_types=sqlite3.PARSE_DECLTYPES |\
                            sqlite3.PARSE_COLNAMES)
c = conn.cursor()
c.execute('PRAGMA journal_mode = WAL')
c.row_factory = sqlite3.Row

table_name = 'node_000'
schema = '(Timestamp TIMESTAMP UNIQUE,Readings REAL)'
cmd = 'CREATE TABLE IF NOT EXISTS {} {}'.format(table_name,schema)
c.execute(cmd)


cmd = 'INSERT OR REPLACE INTO node_000 (Timestamp,Readings) VALUES (?,?)'
c.execute(cmd,[datetime.utcnow(),1.23])
c.execute(cmd,[datetime.utcnow(),None])
c.execute(cmd,[datetime.utcnow(),float('nan')])
c.execute(cmd,[datetime.utcnow(),float('inf')])
c.execute(cmd,[datetime.utcnow(),float('-inf')])
conn.commit()

print float('nan')
print float('Nan')
print float('NaN')
print float('NAN')

print float('inf')
print float('Inf')
print float('INF')
print float('-inf')






