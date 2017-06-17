"""
Data objects
"""
import classes.MongoManager

class Page():
    def __init__(self, page, urls):
        self.num = page
        self.urls = urls