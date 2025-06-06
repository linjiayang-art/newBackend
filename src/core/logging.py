import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask import request,current_app
from flask.logging import default_handler
import time
from src.settings import basedir


def register_logging(app:Flask):
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super().format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    year_month=time.strftime("%Y-%m-%d", time.localtime())
    
    file_handler = RotatingFileHandler(os.path.join(app.config['LOG_DIR'], f'{year_month}.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # mail_handler = SMTPHandler(
    #     mailhost=app.config['MAIL_SERVER'],
    #     fromaddr=app.config['MAIL_USERNAME'],
    #     toaddrs=['ADMIN_EMAIL'],
    #     subject='Greybook Application Error',
    #     credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    # mail_handler.setLevel(logging.ERROR)
    # mail_handler.setFormatter(request_formatter)

    if not app.debug:
        # app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)
    else:
        # app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(default_handler)

        