from bs4 import BeautifulSoup as bs
import lxml
import re
import datetime
import DataObjects


base_url = 'https://www.xvideos.com'

def getLinks(pageData):
    pageData = re.sub('<script>*?</script>', '', str(pageData))
    parse = bs(pageData, 'html5lib')
    #remove script tags
    #[s.extract() for s in parse('script')]
    videos = parse.findAll('div', {'class' : 'thumb-block'})
    urls = []
    for v in videos:
        link = getInfoThumb(v)
        if(link['url'] != None and link['thumb'] != None):
            urls.append(link)
            continue
    return urls

#Get infos from a thumb in a page of videos
def getInfoThumb(v):
    v = removeScript(v)
    v = bs(v, 'html5lib')
    thumb = v.find('img')['src']
    url = base_url + v.find('a')['href']

    return {"url": url, "thumb": thumb}

#Get infos from a video
def getInfoVideo(html, link):
    html = bs(html, 'html5lib')
    parse = html.find('div', {'id' : 'main'})

    #get tags
    tags = []
    tags_parse = parse.find_all('a', {'class' : 'nu'})
    for tag in tags_parse:
        if(tag.text != 'verified profile' and tag.text != 'more tags'):
            tags.append(tag.text)

    #get views and ratings
    infobox = parse.find('div', {'id' : 'video-views-votes'})
    views = infobox.find('strong', {'id' : 'nb-views-number'})
    views = int(views.text.replace(',', ''))
    ratings_total = infobox.find('div', {'class' : 'rating-bar'}).find('span', {'class' : 'total'}).text
    ratings_percent = infobox.find('span', {'class' : 'rating-box'}).find(text=True, recursive=False)
    up_ratings = int(ratings_total) * (float(ratings_percent)/100)
    down_ratings = int(ratings_total) - int(up_ratings)

    #get url, embed, video_id, download_url, duration and title
    head = html.head
    title = head.find('meta', {'property' : 'og:title'})['content']

    duration = int(head.find('meta', {'property' : 'og:duration'})['content'])
    duration = str(datetime.timedelta(seconds=duration))

    vid_id = link[0].split('/')[3][5:]
    download_url = 'https://static-hw.xvideos.com/swf/xv-player.swf?id_video=' + vid_id
    embed = 'https://flashservice.xvideos.com/embedframe/' + vid_id

    video = DataObjects.Video(link[0], title, duration, tags, views, up_ratings, down_ratings, vid_id, download_url, link[3], link[1], link[2])
    return video

def removeScript(v):
    start = '<script>'
    end = '</script>'

    result = re.search('%s(.*)%s' % (start, end), str(v)).group(1)
    return result[43:-5]