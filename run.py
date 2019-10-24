from app import create_app


app = create_app()
# celery = app.celery
if __name__ == '__main__':
	app.run(port=5001,debug=True)