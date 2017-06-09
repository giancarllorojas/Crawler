# -*- coding: utf-8 -*-
import requests

class Requester:
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

    #Get data from URl
    def get(self, url):
        req = requests.get(url, headers=self.headers)
        data = req.text.encode('utf-8')
        if(len(data) > 100):
            return data
        else:
            print("Failed to get URL: " + url)