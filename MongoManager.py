import pymongo
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
from datetime import datetime
import threading

con = None


class MongoManager:
    def __init__(self):
        self.db   = self._get_conn()
        self.mongoLock = threading.Lock()

    def insert(self, video):
        """
        Insert a video dict into mongo
        """
        now = datetime.utcnow()
        video['insertion_date'] = now
        #print(video)
        self.db.videos.insert_one(video)

    def insert_batch(self, list_videos):
        result = {}
        bulk = self.db.videos.initialize_unordered_bulk_op()
        for video in list_videos:
            bulk.insert(video.to_dict())
        self.mongoLock.acquire()
        try:
            result = bulk.execute()
        except pymongo.errors.BulkWriteError as e:
            result = e.details
            print("Total erros: " + str(len(e.details['writeErrors'])))

        print("Total inserted: " + str(result['nInserted']))
        self.mongoLock.release()
        return int(result['nInserted'])
        
        
    def _get_conn(self):
        if(con == None):
            return pymongo.MongoClient('localhost', 27017).pdb
        else:
            return con