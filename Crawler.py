import threading
import queue
from Requester import Requester
from SqLite import SqLite
import sys
import os
import DataObjects

q = queue.Queue()
dbLock = threading.Lock()
sys.path.append('parsers')

class urlInserter(threading.Thread):
    """
    Thread class to be used as a consumer when fetching pages
    """
    def __init__(self, category, parser):
        super(urlInserter, self).__init__()
        self.category = category
        self.parser = parser
        
    def run(self):
        db = SqLite(self.category, self.parser)
        while True:
            page = q.get()
            sys.stdout.write("Saving page " + str(page.num) + " - Total: " + str(len(page.urls)) + "\n")
            db.saveUrls(self.category, self.parser, page.urls)
            #q.task_done()

        db.close()


class Crawler(threading.Thread):
    """
    Thread class to be used to get a range of pages from a determined website
    """
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
            page = DataObjects.Page(p, urls)
            q.put(page)