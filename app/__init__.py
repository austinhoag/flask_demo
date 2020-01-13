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

# dj.config['database.host'] = '127.0.0.1'
# dj.config['database.port'] = 3306
# dj.config['database.user'] = 'ahoag'
# dj.config['database.password'] = 'gaoha'
# if socket.gethostname() == 'braincogs00.pni.princeton.edu':

dj.config['database.user'] = 'ahoag'
dj.config['database.password'] = 'p@sswd'

db_admin = dj.create_virtual_module('admin_demo','ahoag_admin_flask_demo',create_schema=True)

cel = Celery(__name__,broker='amqp://localhost//',
	backend='db+mysql+pymysql://ahoag:p@sswd@localhost:3306/ahoag_celery_test')

def create_app(config_class=Config):
	""" Create the flask app instance"""
	app = Flask(__name__)
	csrf = CSRFProtect(app)

	app.config.from_object(config_class)
	cel.conf.update(app.config)
	from app.main.routes import main
	from app.taskmanager.routes import taskmanager
	app.register_blueprint(main)
	app.register_blueprint(taskmanager)

	return app
