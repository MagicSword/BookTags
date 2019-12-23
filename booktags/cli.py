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
import sys
import click
from flask_migrate import Migrate

from .flaskapp import db, create_app
from .flaskapp.model.models import BookMain, User, Role, Follow, Permission, Post, Comment


# --------------------------------------------------------- common routines

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='./*')
    COV.start()



# main = create_app(os.getenv('FLASK_CONFIG') or 'default')
main = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(main,db)


@main.shell_context_processor
def make_shell_context():
    return dict(db=db, BookMain=BookMain, User=User, Role=Role, Follow=Follow, Permission=Permission, Post=Post, Comment=Comment)
# manager.add_command("shell", Shell(make_context=make_shell_context))



@main.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
@click.argument('test_names', nargs=-1)
def test(coverage, test_names):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    click.echo("=== Start testing ===")
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        html_path = os.path.join(covdir,'index.html')
        print('HTML version: ' % html_path)
        COV.erase()

@main.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # profiledir = os.path.join(basedir, 'tmp/profile')
    main.wsgi_app = ProfilerMiddleware(main.wsgi_app, restrictions=[length],profile_dir=profile_dir)
    # Q:  Warning: Silently ignoring app.run() because the application is run from the flask
    #       command line executable.  Consider putting app.run() behind
    #       an if __name__ == "__main__" guard to silence this warning.
    # A: https://github.com/pallets/flask/pull/2781
    os.environ["FLASK_RUN_FROM_CLI"] = "false"
    main.run(debug=False)


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
   main.run(debug=False)
