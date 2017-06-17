import threading
from classes.Requester import Requester
from classes.SqLite import liteQueue
from classes.SqLite import get_queue
from importlib import import_module
import sys
from classes.MongoManager import MongoManager


qLock       = threading.Lock()
cLock       = threading.Lock()
total_saved = 0

class urlFetcher(threading.Thread):
    """
    Consumer Thread class: Fetches data from a URL, extract its information then save on Mongo
    """
    _pop_amount = 10

    def __init__(self, category, parser, collection, bulk_size):
        super(urlFetcher, self).__init__()
        self.category       = category
        self.origin         = parser
        self.parser         = import_module("parsers." + parser)
        self.req            = Requester()
        self.mongoCon       = {}
        self.collection     = collection
        self.save_amount   = bulk_size

    def run(self):
        buffer  = []
        self.mongoCon = MongoManager(self.collection)
        sq = get_queue(self.category, self.origin)

        while(True):
            qLock.acquire()
            links = sq.pop_many(self._pop_amount)
            qLock.release()

            if(links == None):
                if(len(buffer) > 0):
                    self.save_batch(buffer)
                break

            for link in links:
                html = self.req.get(link[0])
                try:
                    obj = self.parser.parse_page(html, link)
                    buffer.append(obj)
                except Exception as e:
                    print('Error while parsing: ' + str(e))
                    continue

                if(len(buffer) >= self.save_amount):
                    self.save_batch(buffer)
                    buffer = []

        sys.stdout.write("Thread finished: " + str(threading.current_thread().ident) + "\n")

    def save_batch(self, list_obj):
        global total_saved
        num_inserted = self.mongoCon.insert_batch(list_obj)
        cLock.acquire()
        total_saved += num_inserted
        sys.stdout.write("Saved a batch of itens in Mongo. Total: " + str(total_saved) + "\n")
        cLock.release()