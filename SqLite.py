import sqlite3

class SqLite:
    def __init__(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()

    #save to sqlite
    def savePage(self, url, data, origin):
        if(self.verifyPage(url)):
            self.cur.execute("INSERT INTO page VALUES(?, ?, ?)", (url, origin, data))
            self.con.commit()

    #verify if a Page is already on the database
    def verifyPage(self, url):
        self.cur.execute("SELECT * FROM page where url = ?", (url))
        data = self.cur.fetchall()
        if(len(data) > 0):
            return False
        return True

    #verify if a URL is already on the database
    def verifyUrl(self, url):
        self.cur.execute("SELECT * FROM link where url = '" + url + "'")
        data = self.cur.fetchall()
        if(len(data) > 0):
            return False
        return True

    def saveUrls(self, category, urls):
        for url in urls:
            if(self.verifyUrl(url)):
                self.cur.execute("INSERT INTO link VALUES(?, ?, ?, ?)", (url, category, 0, 0))
                self.con.commit()