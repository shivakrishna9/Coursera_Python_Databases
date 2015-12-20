import sqlite3
import urllib
import re

fname = 'mbox-short.txt'

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')


fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.split()
    email = pieces[1]
    email = re.findall('@(.*)' , email)[0]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (email, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) VALUES ( ?, 1 )''', ( email, ) )
    else : 
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', (email, ))
    conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count'
sum = 0
for row in cur.execute(sqlstr) :
    sum = sum + int(row[1])
    print str(row[0]), row[1]

print sum
cur.close()
