from flask import Flask
from flask_celery import make_celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL']='amqp://localhost//',
app.config['CELERY_RESULT_BACKEND']='db+mysql+pymysql://ahoag:p@sswd@localhost:3306/ahoag_celery'

celery = make_celery(app)

@app.route('/process/<name>')
def process(name):

	reverse.delay(name) # starts celery process
	return 'I sent an async request'

@celery.task(name='celery_example.reverse') # if you don't put the name it infers the name for you and sometimes the name is not quite right
def reverse(name):
	return name[::-1]

if __name__ == '__main__':
	app.run(debug=True)