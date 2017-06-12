"""
Fetches the data from a page and get video information
"""
import threading
from Requester import Requester
import queue
from SqLite import SqLite
import sys
from importlib import import_module

q = queue.Queue(maxsize=1000)
mongoLock = threading.Lock()
consumers = []

class sqLiteFetcher(threading.Thread):
    """
    Producer Thread Class: Fetches links from the SqLite then put them into a queue
    """
    def __init__(self, category, parser):
        super(sqLiteFetcher, self).__init__()
        self.category = category
        self.parser = parser
    
    def run(self):
        db = SqLite(self.category, self.parser)
        links = db.getUnfetchedLinks()
        while(True):
            link = links.fetchone()
            if(link == None):
                break
            q.put(link)
            #db.markAsFetched(link[0])

class urlFetcher(threading.Thread):
    """
    Consumer Thread class: Fetches data from a URL, extract information then save on Mongo
    """
    def __init__(self, category, parser):
        super(urlFetcher, self).__init__()
        self.category = category
        self.parser = import_module("parsers." + parser)
        self.req = Requester()

    def run(self):
        while(True):
            link = q.get()
            html = self.req.get(link[0])
            try:
                video_info = self.parser.getInfoVideo(html, link)
            except Exception as e:
                print('Error while parsing video: ' + str(e))
                continue
            mongoLock.acquire()
            sys.stdout.write("Saving video in mongo" + video_info.url + "\n")
            video_info.save()
            mongoLock.release()

            

if(len(sys.argv) < 3):
    print("Fetcher.py category parser num_threads")
    sys.exit()

category = sys.argv[1]
parser = sys.argv[2].strip()
num_threads = int(sys.argv[3])
producer = sqLiteFetcher(category, parser)

producer.start()

for i in range(0, num_threads - 1):
    consumers.append(urlFetcher(category, parser))
    consumers[i].start()

for consumer in consumers:
    consumer.join()

producer.join()