import threading
import queue
from classes.Requester import Requester
from classes.SqLite import liteQueue
from classes.SqLite import get_queue
from importlib import import_module
import sys
import os
import classes.DataObjects as DataObjects

#memory queue
q = queue.Queue(maxsize=1000)
#sqlite queue
sq = None
dbLock = threading.Lock()
sys.path.append('parsers')

class urlInserter(threading.Thread):
    """
    Thread class to be used as a consumer when fetching pages
    """
    def __init__(self, category, parser, num_batch, num_workers):
        super(urlInserter, self).__init__()
        self.category = category
        self.parser = parser
        self.num_batch = num_batch
        self.batch = []
        self.num_workers = num_workers
        
    def run(self):
        sq = get_queue(self.category, self.parser)
        workers_finished = 0
        batches_inserted = 0
        pages_inserted   = 0
        while True:
            page     = q.get()
            url_list = []
            #sys.stdout.write("Saving page " + str(page.num) + " - Total: " + str(len(page.urls)) + "\n")
            if(page == None):
                workers_finished += 1
                sys.stdout.write("Worker finshed, total: " + str(workers_finished) + "\n")
                if(workers_finished == self.num_workers):
                    print("Finish line reached!")
                    sq.put_many(self.batch)
                    break
                else:
                    continue

            for url in page.urls:
                obj = (url['url'], self.category, self.parser, url['thumb'], 0, 0)
                self.batch.append(obj)
            
            pages_inserted += 1

            #insert whole batch
            if(len(self.batch) > self.num_batch):
                sq.put_many(self.batch)
                batches_inserted += 1
                sys.stdout.write("Batch saved. Batches inserted: " + str(batches_inserted) + ", Total pages: " + str(pages_inserted) + "\n")
                self.batch = []


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
        self.parser = import_module("parsers." + parser)
    
    def run(self):
        for p in range(self.start_page, self.end_page):
            url = self.url_start + str(p) + self.url_end
            #sys.stdout.write("Getting URL: " + url + "\n")
            data = self.req.get(url)
            urls = self.parser.parse_pagination(data)
            
            if(urls != None):
                page = DataObjects.Page(p, urls)
                q.put(page)
        sys.stdout.write("Sending poison, thread: " + str(threading.current_thread().ident) + "\n")
        q.put(None)