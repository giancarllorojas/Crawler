from bs4 import BeautifulSoup as bs

base_url = 'https://www.xvideos.com'

def getLinks(pageData):
    parse = bs(pageData, 'html5lib')
    videos = parse.findAll('div', {'class' : 'thumb-block'})
    urls = []
    for v in videos:
        url = getUrl(v)
        if(url != None):
            urls.append(url)
            continue
    return urls

def getUrl(v):
    try:
        tags_p = v.findAll('p')
        p = 0
        for t in tags_p:
            if not (t.has_attr('class')):
                p = t
        if(p != 0):
            url = base_url + p.a['href']
        else:
            url = base_url + "/" + v.get('id') + "/no_title"
        return url
    except Exception as e:
        return None

def getImages(url):
    pass