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
    form = PickCounty()
    states = db.State().fetch('state')
    form.state.choices = [(state,state) for state in states]
    counties = db.County().fetch('county')
    form.county.choices = [(county,county) for county in counties]
       
    if form.validate_on_submit() and request.form['form_name'] == 'PickCounty':
        # code to process form
        flash('state: %s, county: %s' % (form.state.data, form.county.data))
    return render_template('pick_county.html', form=form)

@main.route('/_get_counties/')
def _get_counties():
    state = request.args.get('state', '01', type=str)
    counties = (db.County & f'state="{state}"').fetch('county')
    counties_4json = [(county,county) for county in counties]
    print(counties_4json)
    return jsonify(counties_4json)

# @celery.task(name='celery_example.reverse') # if you don't put the name it infers the name for you and sometimes the name is not quite right
# def reverse(name):
#   return name[::-1]