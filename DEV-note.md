# Development Notes

# Setting UP

```bash
set FLASK_APP=booktags.cli
set FLASK_DEBUG=1
set PROJECT_ADMIN=booktags@example
```

`flask test`

*　models.py change

`flask db migrate -m  "Change what this time"`
`flask db upgrade`
`flask db downgrade` 移除上一次的遷移


pip freeze `pip freeze > requirements.txt
`


# Feature Require

* Flask web ui
* manage database of my own collection(Books,games,musics,movies,files,etc)
    * CURD(Create,Update,Retrieve,Delete)
    * fetch data from online data source(multiple)
* Output booktags PDF    


# Requirement lib
* pymarc - python library for  MARC manager
* marcx - easy extenstion of pymarc
* requests -


# 分工


* isbn ->  libraryid
* libraryid -> MARC
* MARC -> db
* db-design
* 二

用 isbn 查到  MARC ，存到 db
讀 MARC ，存到 db.table 裡

db 

meterial
* book
* disc
* journal 

* ebook
* e-game



# Sub

FrontEnd
1. cli (click)
2. GUI (?)
3. web, flask

BackEnd
1. SQLAlchemy
1. SQLite
2. PostgreSQL
2. MongoDB



Connected to PostgreSQL
[](https://medium.com/jbennetcodes/how-to-use-pandas-to-access-databases-e4e74e6a329e)


pip install psycopy2

from pandas as pd
from sqlalchemy import create_engine

conn = create_engine('postgresql://miller:ming22@localhost:5432/booktags')^M
df = pd.read_sql_table('readmoo_bookshelf', conn)

pd.read_sql_query('show tables', conn)
pd.read_sql_query('select count(*) from payment', conn)
pd.read_sql_query('select * from payment limit 5', conn)














----
library.ylccb.gov.tw

用的系統是  HyLib 整合性圖書館自動化系統 , jsp

[資訊服務採購網 HyLib Lite 圖書館自動化系統(單顆CPU核心數授權)](https://www.cloudmarketplace.org.tw/order/Match/Software/1050204/8/15081)
[Hylib官網](https://solution.hyweb.com.tw/hylib/)


http://library.ylccb.gov.tw/bookSearchList.do?searchtype=simplesearch&execodeHidden=true&execode=&search_field=FullText&search_input=deep+learning
http://library.ylccb.gov.tw/bookSearchList.do?searchtype=simplesearch&execodeHidden=true&execode=&search_field=FullText&search_input=%E6%9D%91%E4%B8%8A%E6%98%A5%E6%A8%B9
http://library.ylccb.gov.tw/bookSearchList.do?searchtype=simplesearch&execodeHidden=true&execode=&search_field=ISBN&search_input=9789864768240


http://library.ylccb.gov.tw/bookSearchList.do?searchtype=simplesearch&execodeHidden=false&execode=&search_field=FullText&search_input=deep+learning

<select id="search_field" name="search_field">
<option value="FullText">全文</option>
<option value="TI">題名 </option>
<option value="PN">個人作者</option>
<option value="PU">出版者 </option>
<option value='CN'>團體作者</option>
<option value="ISBN">ISBN</option>
<option value="SE">叢書名 </option>
<option value="CNO">索書號 </option>
<option value="ACN">條碼號 </option>


<option value='ISSN'>ISSN </option>
<option value='SU'>主題 </option>

http://library.ylccb.gov.tw/bookDetail.do?id=573643

title
author
publisher
CN'>團體作者
isbn
serial
callnumber


http://library.ylccb.gov.tw/exportISOPage.jsp?books=573643

CLASSTYPE
* <option value="CCL">中文圖書分類法</option>
* <option value="DDC">杜威十進分類法</option>
* 美國國家醫學  NLM


var classtype = {"DDC":[{"name":"全部","code":"all"},{"name":"電腦科學、資訊與總類","code":"0"},{"name":"哲學與心理學","code":"1"},{"name":"宗教","code":"2"},{"name":"社會科學","code":"3"},{"name":"語言","code":"4"},{"name":"自然科學","code":"5"},{"name":"技術應用科學","code":"6"},{"name":"藝術與休閒","code":"7"},{"name":"文學","code":"8"},{"name":"歷史、地理與傳記","code":"9"}],"CCL":[{"name":"全部","code":"all"},{"name":"總論","code":"0"},{"name":"哲學類","code":"1"},{"name":"宗教類","code":"2"},{"name":"科學類","code":"3"},{"name":"應用科學類","code":"4"},{"name":"社會科學類","code":"5"},{"name":"史地類","code":"6"},{"name":"世界史地","code":"7"},{"name":"語言文學類","code":"8"},{"name":"藝術類","code":"9"}],"all":[{"name":"全部","code":"all"}]};





Rer:
1. [UNIMarcReader](https://gist.github.com/isergey/1051026)
2. [Schema/Book](https://schema.org/Book)