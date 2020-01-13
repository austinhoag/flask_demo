# config.py
""" This file contains the setup for the app,
for both testing and deployment """

import os
from datetime import timedelta

# The default config
class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY')
	# SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
	CELERY_BROKER_URL='amqp://localhost//',
	CELERY_RESULT_BACKEND='db+mysql+pymysql://ahoag:p@sswd@localhost:3306/ahoag_celery_test'
	CELERYBEAT_SCHEDULE = {
    'job_status_checker': {
        'task': 'app.taskmanager.routes.status_checker',
        'schedule': timedelta(seconds=15)
    },
}
