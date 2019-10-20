import os,sys
from flask import Flask, session
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from celery import Celery

cel = Celery(__name__,broker='amqp://localhost//',
	backend='db+mysql+pymysql://ahoag:p@sswd@localhost:3306/ahoag_celery')

def create_app(config_class=Config):
	""" Create the flask app instance"""
	app = Flask(__name__)
	app.config.from_object(config_class)

	cel.conf.update(app.config)

	from app.main.routes import main

	app.register_blueprint(main)

	return app
