# Develogment log

`python -m booktags` : start flaskapp
or `set FLASK_APP=booktags.cli` then `flask run`
* The name is imported, automatically detecting an app (app) or factory (create_app).
* 系統參考： OReilly.Flask.Web.Development.Developing.Web.Applications.with.Python.2nd.Edition
* 本文記綠每次的更改


# 20220811

* 各package 升級到新版
* itsdangerous.TimedJSONWebSignatureSerializer  在 2.0 版後就[廢棄](https://itsdangerous.palletsprojects.com/en/2.0.x/jws/)了，要改用 [pyjwt](https://pyjwt.readthedocs.io/en/stable/) or [authlib](https://docs.authlib.org/en/latest/index.html)
* [參考方案](https://stackoverflow.com/questions/71292764/which-timed-jsonwebsignature-serializer-replacement-for-itsdangerous-is-better)

# 20220714

* plan to upgrade from flask-bootstrop to bootstrap-flask (support bootstrap4,5)
* 

# 20220712

* booktags/flaskapp/book/forms.py  下的 wtf form 可能需要修改？或加 css?
* booktags/templates/book/edit_book.html 要修？
* https://flask-wtf.readthedocs.io/en/1.0.x/
* https://wtforms.readthedocs.io/en/3.0.x/

# 20220710

* ylclib 更新系統
* 資料庫手動更新到 710
* 資料庫 新增欄位 eisbn，相對改動


# 20191206
* get_link
    * get readmoo links
* .\BookTags\tmp\
* readmoo_bookshelf.csv
    * Readmoo 書藉資料
* bookshelf_callnumber_307.csv(bookshelf_callnumber_307.ods)  
    * 目前書藉資料   
* get_marc.py
    * download marc from ylc.lib
* get_callnumber.py  
    * get callnumber from nbin
* simple_table_grid.py
    * generate A4 booktags
    
# 20191215
* 1. [flask_navbar](https://github.com/zcyuefan/flask-navbar) : 新版的flask-nav
* https://github.com/hack4impact/flask-base
https://stackoverflow.com/questions/57660542/flask-closing-flash-message
https://greyli.com/flask-set-let-flash-message-supports-a-bootstrap-message-style/

# 20191219
* setting 

```python
set FLASK_APP=booktags.cli
set FLASK_DEBUG=1
```
    
# 20191221

* `/docs/conf.py`
* https://opensource.com/article/19/11/document-python-sphinx

# 20191225

* [ward](https://github.com/darrenburns/ward)
* `E:\_Documents\GitHub\PyCharm_Workspace\BookTags>ward`

# 20200110

* pyunimarc: lack of function
* 還是用 pymarc+marcx , 再改成 UNIMARC -> CMARC
* Model design : myAttrib , ReadingStatus