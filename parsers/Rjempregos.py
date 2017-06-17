from bs4 import BeautifulSoup as bs
import lxml
import re
import datetime
from classes.DataObjects import Page
from models.Vaga import Vaga
import re

def parse_pagination(html):
    parse = bs(html, 'html5lib')
    posts = parse.find_all('div', {'class' : 'post'})
    urls = []
    for post in posts:
        try:
            url = post.h1.a['href']
            url = {'url': url, 'thumb': ""}
            urls.append(url)
        except Exception as e:
            pass
            #print(post)
            #print(e)
    return urls

"""
Method for parsing a page and extract its information
"""
def parse_page(html, link):
    parse = bs(html, 'html5lib')
    post  = parse.find('div', {'class' : 'post'})
    title = post.h1.text
    ps    = post.find_all(['p', 'li'])
    text  = ''
    emails = []
    #get text and email
    for p in ps[:-1]:
        text += p.text + '\n'
        match = re.search(r'[\w\.-]+@[\w\.-]+', p.text)
        if(match != None):
            emails.append(match.group(0))

    # clean text
    text = striphtml(text)

    # get date
    try:
        date     = post.find('cite').a['href'].split('/')
        str_date = date[-4] + '/' + date[-3] + '/' + date[-2]
        date     = datetime.datetime.strptime(str_date, '%Y/%m/%d')
    except Exception as e:
        print(e)
        return None

    tags = post.find('cite').find_all('a', {'rel': 'tag'})
    tag_list = []
    if tags != None:
        for tag in tags:
            if(tag != None):
                tag_list.append(tag.text)
    
    vaga = Vaga(link[0], title, text, emails, tag_list, date)
    return vaga

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)