import sqlite3
import sys
import threading

bdLock = threading.Lock()

"""
SqLite Handler class
"""
class SqLite:
    def __init__(self, category, parser):
        conn_url = "databases/" + parser + "_" + category + ".db"
        self.con = sqlite3.connect(conn_url)
        self.cur = self.con.cursor()
        self.createTable()

    def createTable(self):
        try:
            sql = "CREATE TABLE link ( 'url' TEXT UNIQUE,'category'	TEXT,'origin' TEXT, 'thumb' TEXT, 'fetched' INTEGER,'fetched_imgs'	INTEGER,PRIMARY KEY(url));"
            self.cur.execute(sql)
            self.cur.commit()
        except:
            pass

    def saveUrls(self, category, origin, links):
        insert_list = []
        for link in links:
            insert_list.append((link['url'], category, origin, link['thumb'], 0, 0))
            
        bdLock.acquire()
        try:
            self.cur.executemany("INSERT INTO link VALUES(?, ?, ?, ?, ?, ?)", insert_list)
            self.con.commit()
        except Exception as e:
            print(e)
        bdLock.release()

    def getUnfetchedLinks(self):
        sql = "select * from link where fetched = 0"
        return self.cur.execute(sql)

    def markAsFetched(self, url):
        self.cur.execute('update link set fetched=1 where url="' + str(url) + '"')

    def commit(self):
        self.con.commit()     
    
    def close(self):
        self.con.close()