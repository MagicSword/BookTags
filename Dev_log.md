# Develogment log

`python -m booktags` : start flaskapp
or `set FLASK_APP=booktags.cli` then `flask run`
* The name is imported, automatically detecting an app (app) or factory (create_app).




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