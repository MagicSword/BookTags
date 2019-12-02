#coding:UTF-8
import requests
import pandas as pd
import re
import urllib
import time

url = 'http://www.family977.com.tw/News_look.asp?NewsID=724'
webpac = 'http://library.ylccb.gov.tw/webpacIndex.jsp'

r = requests.get(url)
r.text
books_name = re.findall(u'>\u300a(.+?)\u300b(.+?)<',r.text)

print('Total' , len(books_name) , 'books')
books = [x[0] for x in books_name]
#for book in books:
#    print book.encode('utf-8')



lists = books[200:290] # Find the last 5 items

for book in lists:
    #query = urllib.quote(book.encode('utf8'))
    query = '9789864768240'
    headers = {'DNT':'1',
           'Accept-Encoding':'gzip, deflate, sdch',
           'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
           'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Referer':'http://library.ylccb.gov.tw/bookSearchList.do?searchtype=simplesearch&execodeHidden=true&execode=webpac.dataType.book&authoriz=1&search_field=ISBN&search_input=' + query,
           'Cookie':'cookieActived=true; JSESSIONID=92BA9371A15172528F3815B2998B879C; webpacslb-HTTP-80=PDLLFDMA; __utmt=1; __utma=240264336.628942217.1430060220.1430060220.1430060220.1; __utmb=240264336.2.10.1430060220; __utmc=240264336; __utmz=240264336.1430060220.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
           'Connection':'keep-alive'
           }

    url1 = 'http://library.ylccb.gov.tw/booksearch.do?searchtype=simplesearch&execodeHidden=true&execode=webpac.dataType.book&authoriz=1&search_field=ISBN&search_input=' + query
    q1 = requests.get(url1,headers=headers)
    ID1 = re.findall('bookDetail.do\?id=(\d+)' ,q1.text)
    try:
        url2 = 'http://library.ylccb.gov.tw/bookDetail.do?id=' + ID1[0]
        q2 = requests.get(url2,headers=headers)
        ID2 = re.findall('marcid = "(\d+)"',q2.text)
        #ID2 = re.findall('bookDetail.do?id=(\d+)&',q2.text)
        print(book.encode('utf-8'), url1, ID1, ID2)
        if not ID2:
            status1 = 'http://library.ylccb.gov.tw/IntegratHold.do?action=getHold&keepsite=&id=' + ID1[0]
            print(ID1[0])
            df = pd.read_html(status1,encoding='utf=8')
        else:
            status2 = 'http://library.ylccb.gov.tw/IntegratHold.do?action=getHold&keepsite=&id=' + ID2[0]
            print(ID2[0])
            df = pd.read_html(status2,encoding='utf=8')
        #print df[0]
	        #df[0]['book'] = book
        print(df[0][ (df[0][u'典藏館'].str.contains('C01')) & (~df[0][u'館藏位置(到期日期僅為期限，不代表上架日期)'].str.contains(u'已借出')) ])
        print(df[0][ (df[0][u'典藏館'].str.contains('E11')) & (~df[0][u'館藏位置(到期日期僅為期限，不代表上架日期)'].str.contains(u'已借出')) ])
    except:
        print(book.encode('utf-8'), ": 無此書", url1)
    #time.sleep(3)
#
# python Books.py &> tmp
# grep E11 tmp | awk '$3 !~ /NaN/' | sort -k 3