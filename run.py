from app import create_app


app = create_app()
# celery = app.celery
if __name__ == '__main__':
	app.run(host='0.0.0.0',port='8050',debug=True)