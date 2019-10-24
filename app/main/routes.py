from flask import render_template, request, redirect, Blueprint, session, url_for, flash, Markup,Request, jsonify
from app import tasks, db
from .forms import SvgForm, PickCounty


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

@main.route('/pick_county/', methods=['GET', 'POST'])
def pick_county():
    form = PickCounty(form_name='PickCounty')
    form.state.choices = db.State().fetch('state')
    form.county.choices = db.County().fetch('county')
    if request.method == 'GET':
        return render_template('pick_county.html', form=form)
    if form.validate_on_submit() and request.form['form_name'] == 'PickCounty':
        # code to process form
        flash('state: %s, county: %s' % (form.state.data, form.county.data))
    return redirect(url_for('pick_county'))

@main.route('/_get_counties/')
def _get_counties():
    state = request.args.get('state', '01', type=str)
    counties = (db.County & f'state="{state}"').fetch(as_dict=True)
    return jsonify(counties)

# @celery.task(name='celery_example.reverse') # if you don't put the name it infers the name for you and sometimes the name is not quite right
# def reverse(name):
# 	return name[::-1]