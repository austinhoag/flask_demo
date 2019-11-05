from flask import render_template, request, redirect, Blueprint, session, url_for, flash, Markup,Request, jsonify
from app import tasks, db
from .forms import (SvgForm, PickCounty, ExperimentForm,
                    BusinessForm, CustomBusinessForm,
                    CheckboxGridForm, GradeForm, WorkReportForm,
                    ChannelListForm )
from app import tables



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

@main.route('/state_county_js')
def state_county_js():
    return render_template("js/state_county.js")


@main.route("/test_vert_layout") 
def test_vert_layout(): 
    test_data = [{'username':'user1','age':20,'sex':'F'},
                 {'username':'user2','age':22,'sex':'M'},
                 {'username':'user3','age':30,'sex':'F'}]
    table = tables.TestTable(test_data)
    return render_template('test_vertlayout.html',table=table)


@main.route("/test_dynamic_form") 
def test_dynamic_form(): 

    return render_template('dynamic_form.html')    


@main.route("/checkbox_action") 
def checkbox_action(): 

    return render_template('checkbox_action.html')  

@main.route("/dynamic_samples") 
def dynamic_samples(): 
    form = ExperimentForm()
    return render_template('dynamic_samples.html',form=form) 

@main.route('/test_fieldlist', methods=['post','get'])
def test_fieldlist():
    form = BusinessForm()
    if form.validate_on_submit():
        results = []
        for idx, data in enumerate(form.hours.data):
            results.append('{day}: [{open}]:[{close}]'.format(
                day=calendar.day_name[idx],
                open=data["opening"],
                close=data["closing"],
                )
            )
        return render_template('results.html', results=results)
    # print(form.errors)
    hour1_dict = {'opening':'9am','closing':'5pm'}
    hour2_dict = {'opening':'10am','closing':'6pm'}
    hour_dict_list = [hour1_dict,hour2_dict]
    # while len(form.hours) > 0:
    #     form.hours.pop_entry()
    for ii in range(len(hour_dict_list)):
        form.hours.append_entry(hour_dict_list[ii])
    # form.name.data = "Test"
    return render_template('test_fieldlist.html', form=form)

@main.route("/checkbox_getjson") 
def checkbox_getjson(): 
    form = BusinessForm()
    return render_template('checkbox_getjson.html',form=form)

@main.route('/_render_form_fields/')
def _render_form_fields():
    nsamples = request.args.get('nsamples', '1', type=int)
    form = request.args.get('form',type=CustomBusinessForm)
    hour1_dict = {'opening':'9am','closing':'5pm'}
    hour2_dict = {'opening':'10am','closing':'6pm'}
    hour_dict_list = [hour1_dict,hour2_dict]
    print(nsamples)
    print(form)
    for ii in range(len(hour_dict_list)):
        form.hours.append_entry(hour_dict_list[ii])
    # print("in _render_forms()")
    
@main.route('/_generate_form_data/')
def _generate_form_data():
    nsamples = request.args.get('nsamples', '1', type=int)

    data = []
    for ii in range(nsamples):
        hour_dict = {'opening':'%i'%ii,'closing':'5pm','day':ii+1}        
        data.append(hour_dict)
    
    return jsonify(data)

@main.route("/checkbox_getjson_flask",methods=['GET','POST']) 
def checkbox_getjson_flask(): 
    form = CustomBusinessForm()
    if form.validate_on_submit:
        print(form.data)
    return render_template('checkbox_getjson_flask.html',form=form)

@main.route("/checkbox_grid_demo",methods=['GET','POST']) 
def checkbox_grid_demo(): 
    mydata = [{'channel':488,'registration':{'name':'reg_488','value':'reg_488'},
    'injection_detection':{'name':'inj_488','value':'inj_488'}},
              {'channel':555,'registration':{'name':'reg_555','value':'reg_555'},
              'injection_detection':{'name':'inj_555','value':'inj_555'}}]

    tab = tables.CheckBoxTable(mydata)
    return render_template('checkbox_grid_demo.html',table=tab)

@main.route("/checkbox_table_demo",methods=['GET','POST']) 
def checkbox_table_demo(): 
    if request.method == 'GET':
        # form_days = db.session.query(Work_Time).filter_by(user_id=current_user.id).all()
        form_days = [{'index':'0','start_time':'9am','end_time':'10pm'}]
        form = WorkReportForm(days=form_days)
    if request.method == 'POST':
        
        form = WorkReportForm(request.form)
        print(form.data)
        days = []
        # for day in form.days:
        #     print(day.index.data)
            # Work_Time(id = day.index.data,\
            #           user=current_user,\
            #           date=day.date.data,\
            #           start_time=day.start_time.data,\
            #           end_time=day.end_time.data)
    return render_template('checkbox_table_demo.html',form=form)    


@main.route("/channel_table_demo",methods=['GET','POST']) 
def channel_table_demo(): 
    form = ChannelListForm(request.form)

    if request.method == 'GET':
        print("get request")
        # channel_data = [{'channel':'488'},{'channel':'555'},
        # {'channel':'647'},{'channel':'790'}]
        # while len(form.channels) > 0:
        #     form.channels.pop_entry()
        # for ii in range(4):
        #     form.channels.append_entry(channel_data[ii])
        # print(form.data)
    elif request.method == 'POST':
        print("post request")
        print(form.data)
    return render_template('channel_table_demo.html',form=form)     


@main.route("/table_swapper",methods=['GET']) 
def table_swapper(): 
    test_data = [{'username':'user1','age':20,'sex':'F'},
                 {'username':'user2','age':22,'sex':'M'},
                 {'username':'user3','age':30,'sex':'F'}]
    table = tables.TestTable(test_data)
    table.table_id = 'mytable'
    return render_template('table_swapper.html',table=table)       


@main.route("/table_swapper_v2",methods=['GET']) 
def table_swapper_v2(): 
    test_data = [{'username':'user1','age':20,'sex':'F'},
                 {'username':'user2','age':22,'sex':'M'},
                 {'username':'user3','age':30,'sex':'F'}]
    table1 = tables.TestTable(test_data)
    table1.table_id = 'table1'
    table2 = tables.TestTable(test_data)
    table2.table_id = 'table2'
    return render_template('table_swapper_v2.html',table1=table1,table2=table2)   