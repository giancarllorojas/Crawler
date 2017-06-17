import pymongo
from config.config import config                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
from datetime import datetime
import threading

con = None


class MongoManager:
    def __init__(self, collection):
        """
        collection: Name of the collection
        """
        self.db         = self._get_conn()
        self.mongoLock  = threading.Lock()
        self.collection = self.db[collection]

    def insert(self, video):
        """
        Insert a video dict into mongo
        """
        now = datetime.utcnow()
        video['insertion_date'] = now
        #print(video)
        self.collection.insert_one(video)

    def insert_batch(self, list_videos):
        result = {}
        bulk = self.collection.initialize_unordered_bulk_op()
        for video in list_videos:
            bulk.insert(video.to_dict())
        self.mongoLock.acquire()
        try:
            result = bulk.execute()
        except pymongo.errors.BulkWriteError as e:
            result = e.details
            print("Total erros: " + str(len(e.details['writeErrors'])))
        self.mongoLock.release()
        return int(result['nInserted'])
        
    def _get_conn(self):
        if(con == None):
            return pymongo.MongoClient(config['host'], config['port']).pdb
        else:
            return con