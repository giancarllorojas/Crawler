from Requester import Requester
from SqLite import SqLite
import sys
sys.path.append('parsers')

class Crawler:
    def __init__(self, category, url_start, url_end, parser):
        self.category = category
        self.url_start = url_start
        self.url_end   = url_end
        self.req = Requester()
        self.parser = __import__(parser)
        self.db = SqLite()
    
    def run(self, start, end):
        for p in range(start, end):
            url = self.url_start + str(p) + self.url_end
            print("Getting URL: " + url)
            data = self.req.get(url)
            urls = self.parser.getLinks(data)
            print("Saving page " + str(p) + " - Total: " + str(len(urls)), end='')
            self.db.saveUrls(self.category, urls)
            print(" - done")



c = Crawler('real_amateur', 'https://www.xvideos.com/c/', '/real_amateur-17', 'Xvideos')

c.run(50,250)