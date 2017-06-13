"""
Fetches the data from a page and get video information
"""
import threading
from Requester import Requester
from SqLite import liteQueue
from SqLite import get_queue
import sys
from importlib import import_module
from MongoManager import MongoManager

qLock       = threading.Lock()
cLock       = threading.Lock()
consumers   = []
total_saved = 0

class urlFetcher(threading.Thread):
    """
    Consumer Thread class: Fetches data from a URL, extract its information then save on Mongo
    """
    _save_amount = 50
    _pop_amount = 10

    def __init__(self, category, parser):
        super(urlFetcher, self).__init__()
        self.category = category
        self.origin = parser
        self.parser = import_module("parsers." + parser)
        self.req = Requester()
        self.total_fetched = 0
        self.mongoCon = {}

    def run(self):
        buffer_video  = []
        self.mongoCon = MongoManager()
        sq = get_queue(self.category, self.origin)

        while(True):
            qLock.acquire()
            links = sq.pop_many(self._pop_amount)
            qLock.release()

            if(links == None):
                if(len(buffer_video) > 0):
                    self.save_batch(buffer_video)
                break

            for link in links:
                html = self.req.get(link[0])
                try:
                    video = self.parser.getInfoVideo(html, link)
                    buffer_video.append(video)
                except Exception as e:
                    print('Error while parsing video: ' + str(e))
                    continue

                #print(len(buffer_video), self._save_amount)
                if(len(buffer_video) >= self._save_amount):
                    self.save_batch(buffer_video)
                    buffer_video = []

        sys.stdout.write("Thread finished: " + str(threading.current_thread().ident) + "\n")

    def save_batch(self, list_videos):
        global total_saved
        sys.stdout.write("Saving a batch of videos in Mongo. Total: " + str(total_saved) + "\n")
        num_inserted = self.mongoCon.insert_batch(list_videos)
        cLock.acquire()
        total_saved += num_inserted
        cLock.release()

            

if(len(sys.argv) < 3):
    print("Fetcher.py category parser num_threads")
    sys.exit()

category = sys.argv[1]
parser = sys.argv[2].strip()
num_threads = int(sys.argv[3])
#producer = sqLiteFetcher(category, parser, num_threads)

#producer.start()

for i in range(0, num_threads):
    consumers.append(urlFetcher(category, parser))
    consumers[i].start()

for consumer in consumers:
    consumer.join()

#producer.join()