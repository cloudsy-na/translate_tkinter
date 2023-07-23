import sqlite3

#backend


def TransData():
    con = sqlite3.connect("translate update.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS datakamus (id INTEGER PRIMARY KEY, kata char(200), arti char(200), flag integer default Yes, sqltime timestamp default current_timestamp, sqltimeupdate timestamp default current_timestamp)")
    con.commit()
    con.close()

def AddData(kata, arti, flag, sqltime, sqltimeupdate):
    con = sqlite3.connect("translate update.db")
    cur = con.cursor()
    cur.execute("INSERT INTO datakamus VALUES (NULL, ?, ?, ?, ?, ?)", (kata, arti, flag, sqltime, sqltimeupdate))
    con.commit()
    con.close()

def ViewData():
    con = sqlite3.connect("translate update.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM datakamus")
    rows = cur.fetchall()
    con.close()
    return rows

def DeleteData(id):
    con = sqlite3.connect("translate update.db")
    cur = con.cursor()
    cur.execute("DELETE FROM datakamus WHERE id=?",(id,))
    con.commit()
    con.close()

def UpdateData(kata, arti, flag, sqltime, sqltimeupdate, id):
    con = sqlite3.connect("translate update.db")
    cur = con.cursor()
    cur.execute("UPDATE datakamus SET kata = ?, arti = ?, flag = ?, sqltime = ?, sqltimeupdate = ? WHERE id = ?",(kata, arti, flag, sqltime, sqltimeupdate, id))
    con.commit()
    con.close()

TransData()
    
