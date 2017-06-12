"""
Object that represents a video
"""
import MongoManager

class Video():
    def __init__(self, url, title, duration, tags, origin_views, origin_upvotes, origin_downvotes, origin_vid_id, download_url, thumb, category, origin_name):
        self.url = url
        self.title = title
        self.duration = duration
        self.tags = tags
        self.category = category
        self.origin = Video_Origin(origin_name, origin_views, origin_upvotes, origin_downvotes, origin_vid_id)
        self.thumb = thumb
        self.comments = []
        self.download_url = download_url
        self.rating = {
            "up": 0,
            "down": 0
        }
        
    
    def save(self):
        try:
            dict_obj = self.__dict__
            dict_obj['origin'] = self.origin.__dict__
            MongoManager.con.insertVideo(dict_obj)
        except Exception as e:
            print(e)

class Video_Origin():
    def __init__(self, name, views, upvotes, downvotes, vid_id):
        self.name = name
        self.views = views
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.vid_id = vid_id

class Page():
    def __init__(self, page, urls):
        self.num = page
        self.urls = urls