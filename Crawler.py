import threading
import queue
from Requester import Requester
from SqLite import SqLite
import sys
import os

q = queue.Queue()
dbLock = threading.Lock()
sys.path.append('parsers')

class Page():
    def __init__(self, page, urls):
        self.num = page
        self.urls = urls

class urlInserter(threading.Thread):
    def __init__(self, category, origin):
        super(urlInserter, self).__init__()
        self.category = category
        self.origin = origin
        
    def run(self):
        db = SqLite()
        while True:
            page = q.get()
            sys.stdout.write("Saving page " + str(page.num) + " - Total: " + str(len(page.urls)) + "\n")
            db.saveUrls(self.category, self.origin, page.urls)
            q.task_done()
        db.close()

class Crawler(threading.Thread):
    def __init__(self, category, url_start, url_end, start, end, parser):
        super(Crawler, self).__init__()
        self.category = category
        self.url_start = url_start
        self.url_end   = url_end
        self.start_page = start
        self.end_page = end
        self.req = Requester()
        self.origin = parser
        self.parser = __import__(parser)
    
    def run(self):
        for p in range(self.start_page, self.end_page):
            url = self.url_start + str(p) + self.url_end
            #sys.stdout.write("Getting URL: " + url + "\n")
            data = self.req.get(url)
            urls = self.parser.getLinks(data)
            page = Page(p, urls)
            q.put(page)