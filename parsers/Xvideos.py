from bs4 import BeautifulSoup as bs

base_url = 'https://www.xvideos.com/'

def getLinks(pageData):
    parse = bs(pageData, 'html5lib')
    videos = parse.findAll('div', {'class' : 'thumb-block'})
    urls = []
    for v in videos:
        try:
            url = base_url + v.find('a')['href']
            urls.append(url)
        except:
            print("Failed to get link")
    return urls

def getImages(url):
    pass