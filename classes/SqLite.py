import sqlite3
import sys
import threading
from time import sleep

sq = None

def get_queue(category, parser):
    if sq == None:
        return liteQueue(category, parser)
    return sq

"""
SqLite Job Handler class for Links
"""
class liteQueue:
    _create         = "CREATE TABLE IF NOT EXISTS link ( 'url' TEXT,'category'	TEXT,'origin' TEXT, 'thumb' TEXT, 'fetched' INTEGER,'fetched_imgs'	INTEGER,PRIMARY KEY(url));"
    _putList        = "INSERT OR IGNORE INTO link VALUES(?, ?, ?, ?, ?, ?)"
    _iterate        = "SELECT * FROM LINK WHERE FETCHED = 0"
    _write_lock     = "BEGIN IMMEDIATE"
    _pop_get_many   = "SELECT URL, CATEGORY, ORIGIN, THUMB, ROWID FROM LINK WHERE FETCHED = 0 ORDER BY ROWID ASC LIMIT "
    _pop_del_many   = "UPDATE LINK SET FETCHED=1 WHERE FETCHED = 0 AND (ROWID >= ? AND ROWID <=?)"

    def __init__(self, category, parser):
        self.conn_url = "databases/" + parser + "_" + category + ".db"
        self._connection_cache = {}
        with self._get_conn() as conn:
            conn.execute(self._create)
    
    def _get_conn(self):
        id = threading.current_thread().ident
        if id not in self._connection_cache:
            self._connection_cache[id] = sqlite3.Connection(self.conn_url, timeout=60)
        return self._connection_cache[id]

    def __iter__(self):
        with self._get_conn() as conn:
            for result in conn.execute(self._iterate):
                yield result
    
    def put_many(self, list_obj):
        with self._get_conn() as conn:
            try:
                conn.cursor().executemany(self._putList, list_obj)
            except Exception as e:
                print(e)
                
    def pop_many(self, amount, sleep_wait=True):
        keep_pooling = True
        sql_pop = self._pop_get_many + str(amount)
        with self._get_conn() as conn:
            result = None
            while keep_pooling:
                conn.execute(self._write_lock) # lock the database
                cursor = conn.execute(sql_pop)
                result = cursor.fetchall()

                if(len(result) > 0):
                    keep_pooling = False
                    id_first = int(result[0][4])
                    id_last  = int(result[-1][4])
                    conn.execute(self._pop_del_many, (id_first, id_last))
                    conn.commit() # unlock the database
                    return result
                else:
                    conn.commit() # unlock the database
                    return None