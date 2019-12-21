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

import os
import click
from flask_migrate import Migrate

from .flaskapp import db, create_app
from .flaskapp.model.models import BookMain, User, Role, Follow, Permission, Post


# --------------------------------------------------------- common routines

# main = create_app(os.getenv('FLASK_CONFIG') or 'default')
main = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(main,db)


@main.shell_context_processor
def make_shell_context():
    return dict(db=db, BookMain=BookMain, User=User, Role=Role, Follow=Follow, Permission=Permission, Post=Post)
# manager.add_command("shell", Shell(make_context=make_shell_context))



@main.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Some doc here"""
    click.echo("Start testing")
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)




@main.cli.command()
def initdb():
    click.echo("Hello model")


@main.cli.command()
def list_routes():
    import urllib

    output = []
    for rule in main.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)


# @click.command()
# @click.argument("name")
# def hello_user(name):
#     print("Hello! %s" % name)



# @cli.command("flask", short_help="run flask app.")
# @click.option("run", "-r", help="run flask app.")
# @click.pass_context
# def flask_run():
# #     app = create_app()
#     print("flask run here")

if __name__ == '__main__':
    pass
