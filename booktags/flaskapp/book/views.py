#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    example.py
    ~~~~~~~~~
    A simple command line application to run flask apps.
    :copyright: 2019 Miller
    :license: BSD-3-Clause
"""

# Known bugs that can't be fixed here:
#   - synopsis() cannot be prevented from clobbering existing
#     loaded modules.
#   - If the __file__ attribute on a module is a relative path and
#     the current directory is changed with os.chdir(), an incorrect
#     path will be displayed.



from flask import render_template, redirect, request, url_for, flash,jsonify,current_app
from flask_login import login_user, logout_user, login_required, current_user

from . import book
from flask_sqlalchemy import get_debug_queries
from sqlalchemy.sql.expression import cast
from datatables import ColumnDT, DataTables

from .. import auth
from .. import db

from .forms import EditBookForm, HackmdMeta
# from booktags.db.basemodels import Book
from booktags.flaskapp.model.models import BookMain

# --------------------------------------------------------- common routines

@book.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['PROJECT_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@book.route('/', methods=['GET', 'POST'])
def index():
    # books=BookMain.get_all_book()
    query = BookMain.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(cast(BookMain.id, db.Integer)).paginate(
        page, per_page=current_app.config['PROJECT_BOOKS_PER_PAGE'],
        error_out=False)
    books = pagination.items
    return render_template('book/index.html',books=books,pagination=pagination)

# @book.route('/list/', methods=['GET', 'POST'])
# def list_book():
#     """
#
#     :param field: col name
#     :param order: asc or desc
#     :return: renew query
#     """
#     books = BookMain.get_all_book()
#     return render_template('book/list_book.html',books=books)

@book.route("/list")
def list_book():
    """List users with DataTables <= 1.10.x."""
    return render_template('book/list_book.html')


@book.route('/data', methods=['GET', 'POST'])
def data():
    """Return server side data."""
    # defining columns
    #  - explicitly cast date to string, so string searching the date
    #    will search a date formatted equal to how it is presented
    #    in the table
    columns = [
        # ColumnDT(cast(BookMain.id, db.Integer)),
        ColumnDT(BookMain.id),
        ColumnDT(BookMain.isbn),
        ColumnDT(BookMain.title_short),
        ColumnDT(BookMain.title),
        ColumnDT(BookMain.catalogue),
        ColumnDT(BookMain.cutter),
        ColumnDT(BookMain.pub_year),
        ColumnDT(BookMain.copy_info)
        # ColumnDT(BookMain.get_link),
        # ColumnDT(BookMain.note),
        # ColumnDT(BookMain.reprint),
        # ColumnDT(BookMain.removed),
        # ColumnDT(BookMain.keepsite)
    ]

    # defining the initial query depending on your purpose
    query = db.session.query().select_from(BookMain)


    # GET parameters
    params = request.args.to_dict()


    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)

    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())



@book.route('/get/<int:id>', methods=['GET', 'POST'])
def get_book():
    return f"Hello book index : {id}"


@book.route('/post/', methods=['GET', 'POST'])
def post_book():
    """
    post new book entry
    :return:
    """
    book = BookMain.query.all()
    id = int(book[-1].id) + 1
    print(f"id is : {id}")
    form = EditBookForm()
    if form.validate_on_submit():
        book.id = form.id.data
        book.isbn = form.isbn.data
        book.title_short = form.title_short.data
        book.title = form.title.data
        book.catalogue = form.catalogue.data
        book.cutter = form.cutter.data
        book.pub_year = form.pub_year.data
        book.copy_info = form.copy_info.data
        book.get_link = form.get_link.data
        book.note = form.note.data
        book.reprint = form.reprint.data
        book.removed = form.removed.data
        book.keepsite = form.keepsite.data

        db.session.add(book)
        db.session.commit()
        flash('Your book data has been added.', 'success')
        return redirect(url_for('book.index'))
    form.id.data = id
    return render_template('book/edit_book.html', form=form)


@book.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    """
    edit ,  put book data
    :param id:
    :return:
    """
    form = EditBookForm()
    book = BookMain.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        # book.id = form.id.data
        book.isbn = form.isbn.data
        book.title_short = form.title_short.data
        book.title = form.title.data
        book.catalogue = form.catalogue.data
        book.cutter = form.cutter.data
        book.pub_year = form.pub_year.data
        book.copy_info = form.copy_info.data
        book.get_link = form.get_link.data
        book.note = form.note.data
        book.reprint = form.reprint.data
        book.removed = form.removed.data
        book.keepsite = form.keepsite.data

        db.session.add(book)
        db.session.commit()
        flash('Your book data has been updated.', 'success')
        return redirect(url_for('book.index'))
    form.id.data = book.id
    form.isbn.data = book.isbn
    form.title_short.data = book.title_short
    form.title.data = book.title
    form.catalogue.data = book.catalogue
    form.cutter.data = book.cutter
    form.pub_year.data = book.pub_year
    form.copy_info.data = book.copy_info
    form.get_link.data = book.get_link
    form.note.data = book.note
    form.reprint.data = book.reprint
    form.removed.data = book.removed
    form.keepsite.data = book.keepsite
    return render_template('book/edit_book.html', form=form)

@book.route('/del/<int:id>', methods=['GET', 'POST'])
def del_book(id):
    return f"Hello book index: del {id}"

@book.route('/hackmdmeta', methods=['GET', 'POST'])
def hackmd_meta():
    """
    
    :return: 
    """
    from booktags.vendor.hackmd_meta import get_hackmdmeta
    form = HackmdMeta()
    if form.validate_on_submit():
        booksn = str(form.booksn.data)
        # print(f"booksn is : {booksn}")
        temp = get_hackmdmeta(booksn)
        # print(temp)
        form.body.data = temp

        # flash('Your book data has been updated.', 'success')
        # return redirect(url_for('book.hackmd_meta'))


    return render_template('book/hackmd_meta.html',form=form)


if __name__ == '__main__':
    pass
