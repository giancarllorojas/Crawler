import Utils.hash_utils
from datetime import datetime

class Video:
    def __init__(self, url, title, duration, tags, origin_views, origin_upvotes, origin_downvotes, origin_vid_id, download_url, thumb, category, origin_name):
        self.url            = url
        self.ident          = Utils.hash_url(url)
        self.title          = title
        #only in seconds
        self.duration       = int(duration)
        self.tags           = tags
        self.insertion_date = datetime.utcnow()
        self.category       = category
        self.origin         = Video_Origin(origin_name, origin_views, origin_upvotes, origin_downvotes, origin_vid_id)
        self.thumb          = thumb
        self.comments       = []
        self.download_url   = download_url
        self.rating         = {
            "up": 0,
            "down": 0
        }
    
    def to_dict(self):
        try:
            dict_obj = self.__dict__
            dict_obj['origin'] = self.origin.__dict__
            return dict_obj
        except Exception as e:
            print(e)

    def __str__(self):
        return self.url

class Video_Origin():
    def __init__(self, name, views, upvotes, downvotes, vid_id):
        self.name = name
        self.views = views
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.vid_id = vid_id