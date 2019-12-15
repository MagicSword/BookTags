# Development Notes

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


<span id="simplesearchkeepsite">
								<label title="館藏地/室">館藏地/室：</label>
								<select id="keepsitelimit">

									<option value=""> 請選擇</option>

									<option value="EL"> 二崙鄉立圖書館</option>

									<option value="KH"> 口湖鄉立圖書館</option>

									<option value="TK"> 土庫鎮立圖書館</option>

									<option value="TKMG"> 土庫鎮馬光分館</option>

									<option value="TP"> 大埤鄉立圖書館</option>

									<option value="YC"> 元長鄉立圖書館</option>

									<option value="YLJ"> 文化處兒童室</option>

									<option value="YLR"> 文化處參考室</option>

									<option value="YLS"> 文化處視聽期刊室</option>

									<option value="YL"> 文化處圖書室</option>

									<option value="TM"> 斗六市中山分館</option>

									<option value="TL"> 斗六市立繪本館</option>

									<option value="TN"> 斗南鎮立圖書館</option>

									<option value="CL"> 水林鄉立圖書館</option>

									<option value="PK"> 北港鎮立圖書館</option>

									<option value="KC"> 古坑鄉立圖書館</option>

									<option value="TC"> 台西鄉立圖書館</option>

									<option value="SH"> 四湖鄉立圖書館</option>

									<option value="SL"> 西螺鎮立圖書館</option>

									<option value="DC"> 東勢鄉立圖書館</option>

									<option value="LN"> 林內鄉立圖書館</option>

									<option value="HW"> 虎尾鎮立圖書館</option>

									<option value="LB"> 崙背鄉立圖書館</option>

									<option value="ML"> 麥寮鄉立圖書館</option>

									<option value="YLD"> 雲林分區資源中心</option>

									<option value="GTMY"> 莿桐鄉麻園分館</option>

									<option value="BC"> 褒忠鄉立圖書館</option>



								</select>
							</span>



							<label title="特藏">特藏：</label>
			<select name="cln" id="clnSelect">
			<option value="all" >全部</option>

				<option value="B" >一般圖書</option>

				<option value="RJ" >不可外借兒童書</option>

				<option value="JPN" ></option>

				<option value="PAD" >平板電腦</option>

				<option value="LJ" >幼兒圖書</option>

				<option value="LJE" >幼兒圖書(西文)</option>

				<option value="IND" >印尼圖書</option>

				<option value="IN" ></option>

				<option value="L" >地方文獻</option>

				<option value="M" >地圖</option>

				<option value="RE" >西文參考書</option>

				<option value="E" >西文圖書</option>

				<option value="TBC" >巡迴書箱(咖啡)</option>

				<option value="TBS" >巡迴書箱(學校)</option>

				<option value="J" >兒童書</option>

				<option value="JE" >兒童書(西文)</option>

				<option value="OT" >其它</option>

				<option value="YA" >青少年</option>

				<option value="CAM" >柬埔寨</option>

				<option value="XX" >活動用書</option>

				<option value="THA" >泰國</option>

				<option value="MAY" >馬來西亞</option>

				<option value="R" >參考書</option>

				<option value="PR" >推廣閱讀</option>

				<option value="S" >期刊</option>

				<option value="RP" >菲律賓</option>

				<option value="VIE" >越南圖書</option>

				<option value="YL" >雲林文獻</option>

				<option value="JYL" >雲林縣政府出版品：兒童</option>

				<option value="SL" >微縮軟片</option>

				<option value="N" >新書</option>

				<option value="CD" >雷射唱片</option>

				<option value="LD" >雷射影碟</option>

				<option value="BA" >圖書附件</option>

				<option value="CM" >漫畫書</option>

				<option value="OB" >銀髮族</option>

				<option value="LAO" >寮國</option>

				<option value="VCD" >影音壓縮光碟</option>

				<option value="DVD" >數位影音光碟(DVD )</option>

				<option value="NDVD" >數位影音光碟</option>

				<option value="MV" >樂譜</option>

				<option value="BUR" >緬甸</option>

				<option value="AC" >錄音帶</option>

				<option value="VC" >錄影帶</option>

				<option value="SB" >館藏特色叢書</option>

				<option value="BD" >藍光光碟</option>

				<option value="GB" >贈書</option>

			</select>
		</p>


Rer:
1. [UNIMarcReader](https://gist.github.com/isergey/1051026)
2. [Schema/Book](https://schema.org/Book)