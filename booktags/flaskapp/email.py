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

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

from ..logger import create_logger

# --------------------------------------------------------- common routines

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    # logging
    logger = create_logger("")
    logger.info('Start logging email: \n')

    try:
        pass
    except Exception as e:
        logger.exception("Runtime Error Message:")
    logger.info("email.py info:")
    logger.info(f"to: {to}")
    logger.info(f"subject: {subject}")
    logger.info(f"template: {template}")
    # end logging


    app = current_app._get_current_object()
    msg = Message(app.config['PROJECT_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['PROJECT_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


if __name__ == '__main__':
    pass