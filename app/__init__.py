import os,sys
from flask import Flask, session
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
import datajoint as dj
from flask_wtf.csrf import CSRFProtect
import socket

dj.config['database.host'] = '127.0.0.1'
dj.config['database.port'] = 3306
dj.config['database.user'] = 'ahoag'

if socket.gethostname() == 'braincogs00.pni.princeton.edu':
	dj.config['database.password'] = 'gaoha'
else:
	dj.config['database.password'] = 'p@sswd'

db = dj.create_virtual_module('ahoag_flask_demo','ahoag_flask_demo',create_schema=True) # creates the schema if it does not already exist. Can't add tables from within the app because create_schema=False


cel = Celery(__name__,broker='amqp://localhost//',
	backend='db+mysql+pymysql://ahoag:p@sswd@localhost:3306/ahoag_celery')

def create_app(config_class=Config):
	""" Create the flask app instance"""
	app = Flask(__name__)
	csrf = CSRFProtect(app)

	app.config.from_object(config_class)

	cel.conf.update(app.config)

	from app.main.routes import main

	app.register_blueprint(main,url_prefix="/dogs")

	return app
