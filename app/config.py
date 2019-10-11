# config.py
""" This file contains the setup for the app,
for both testing and deployment """

import os

# The default config
class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
	SQLALCHEMY_TRACK_MODIFICATIONS = False # to turn that annoying warning off
