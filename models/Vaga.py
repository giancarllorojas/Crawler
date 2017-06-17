from utils.hash_utils import hash_url
from datetime import datetime

class Vaga:
    def __init__(self, url, title, text, emails, tags, date):
        self.url            = url
        self.ident          = hash_url(url)
        self.title          = title
        self.text           = text
        self.emails         = emails
        self.date           = date
        self.tags           = tags
        self.insertion_date = datetime.utcnow()

    def to_dict(self):
        return self.__dict__