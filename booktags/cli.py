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

import click
from .flaskapp import create_app

# --------------------------------------------------------- common routines



@click.command()
#@click.option('-r','--run', help= "run flask app")
def cli(*args, **kwargs):
    """Some doc here"""
    click.echo("Hello, cli")
    click.echo("Start flask app")
    app = create_app()
    app.run(debug=True)



@click.command()
@click.argument("name")
def hello_user(name):
    print("Hello! %s" % name)



# @cli.command("flask", short_help="run flask app.")
# @click.option("run", "-r", help="run flask app.")
# @click.pass_context
# def flask_run():
# #     app = create_app()
#     print("flask run here")

if __name__ == '__main__':
    pass
