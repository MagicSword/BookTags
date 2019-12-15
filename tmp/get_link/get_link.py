"""
get readmoo isbn

TODO: save file

登入問題，所以用預先存下來的書本列表 html , 1.html, 2,html, 3.html
books: globe list



"""


import requests
from bs4 import BeautifulSoup
import re
import time

BASEPATH = "E:\_Documents\GitHub\PyCharm_Workspace\scrapy_test\get_link\get\\"

books = []
count = 0

def url_to_isbn(url):
    """
    url: readmoo book url
    isbn: readmoo book isbn
    有些書可能沒有 isbn, 所以加上 try ,except
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    isbn = ''
    try:
        isbn = soup.find_all('span',{"itemprop":"ISBN"})[0].text
    except IndexError:
        print("No ISBN: {}".format(url))
        return '0'
    else:
        return isbn


for i in range(1,4):
    path = BASEPATH + str(i) + '.html'
    with open(path,'r',encoding='UTF-8') as fd:
        soup = BeautifulSoup(fd.read())
        for book_cover in soup.findAll("div", {"class": "book-cover"}):
            link = book_cover.select('a')[1]["href"] 
            #img_url = book-cover.select('img')[0]["src"]
            title = book_cover.select('img')[0]["title"]
            count = count + 1
            isbn = url_to_isbn(link)
            # print('{} title : {}'.format(count,title))
            # print('   link  : {}'.format(link))
            print("{count} : {isbn}".format(count=count,isbn=isbn))
            element = {"id": count,"title": title,"isbn": isbn,"link": link}
            books.append(element)
            if count >= 20:
                  time.sleep(1)
            
print(len(books))


if "__name__" == "__main__":
    pass



