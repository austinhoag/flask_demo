import os,sys
from flask import Flask, session
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

def create_app(config_class=Config):
	""" Create the flask app instance"""
	app = Flask(__name__)
	app.config.from_object(config_class)

	# db.init_app(app)
	# login_manager.init_app(app)
	# from lightserv.users.routes import users
	from app.main.routes import main

	app.register_blueprint(main)

	return app
