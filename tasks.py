from celery import Celery
import time

cel_app = Celery('tasks',broker='amqp://localhost//',backend='db+mysql+pymysql://ahoag:p@sswd@localhost:3306/ahoag_celery')

@cel_app.task
def reverse(string):
	time.sleep(10)
	return string[::-1]
