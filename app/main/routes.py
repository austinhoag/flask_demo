from flask import render_template, request, redirect, Blueprint, session, url_for, flash, Markup,Request
from app import tasks
from .forms import SvgForm

main = Blueprint('main',__name__)

# from app import celery

@main.route("/") 
@main.route("/home") 
def home(): 
	form = SvgForm()
	return render_template('home.html',form=form)

@main.route('/process/<name>')
def process(name):

	tasks.reverse.delay(name) # starts celery process
	return 'I sent an async request'

# @celery.task(name='celery_example.reverse') # if you don't put the name it infers the name for you and sometimes the name is not quite right
# def reverse(name):
# 	return name[::-1]