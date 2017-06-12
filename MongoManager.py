import pymongo
from datetime import datetime

class MongoManager:
    def __init__(self):
        self.db = pymongo.MongoClient('localhost', 27017).pdb

    def insertVideo(self, video):
        """
        Insert a video dict into mongo
        """
        now = datetime.utcnow()
        video['insertion_date'] = now
        #print(video)
        self.db.videos.insert_one(video)
        

con = MongoManager()