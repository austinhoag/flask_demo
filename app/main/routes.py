from flask import (render_template, request, redirect, Blueprint,
                   session, url_for, flash, Markup,Request,
                   jsonify, send_file)
from app import tasks, db
from .forms import (SvgForm, PickCounty, ExperimentForm,
                    BusinessForm, CustomBusinessForm,
                    CheckboxGridForm, GradeForm, WorkReportForm,
                    ChannelListForm, ExpForm, StateForm )
from app import tables
from app.main.utils import do_plot, table_sorter
import pandas as pd
import logging

from functools import partial

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

''' Make the file handler to deal with logging to file '''
file_handler = logging.FileHandler('logs/experiment_routes.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler() # level already set at debug from logger.setLevel() above

stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

main = Blueprint('main',__name__)

# from app import celery

@main.route("/") 
@main.route("/home") 
def home(): 
    form = SvgForm()
    return render_template('home.html',form=form)

@main.route("/demo")
def demo():
    return render_template('demo.html')

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


@main.route("/table_swapper_v3",methods=['GET']) 
def table_swapper_v3(): 
    test_data = [{'username':'user1','age':20,'sex':'F'},
                 {'username':'user2','age':22,'sex':'M'},
                 {'username':'user3','age':30,'sex':'F'}]
    table1 = tables.TestTable(test_data)
    table1.table_id = 'vertical'
    table2 = tables.TestTable(test_data)
    table2.table_id = 'horizontal1'
    return render_template('table_swapper_v3.html',table1=table1,table2=table2)   

@main.route("/new_exp/",methods=['GET','POST']) 
def new_exp(): 
    # custom_clearing = request.args.get('custom_clearing',0)
    form = ExpForm(request.form)
    custom_clearing=None
    if form.validate_on_submit():
        print("validated")
        if form.custom_clearing_submit.data == True:
            custom_clearing = 1
            for ii in range(form.number_of_samples.data):
                form.clearing_samples.append_entry()
        elif form.uniform_clearing_submit.data == True:
            custom_clearing = 0 
            form.clearing_samples.append_entry()
        

        # redirect_url = '%s?custom_clearing=1' % url_for('main.new_exp')
        # return redirect(redirect_url)
    else:
        print(form.errors)
    if 'column_name' not in locals():
        column_name = ''
    print("custom_clearing =", custom_clearing)
    return render_template('experiments/new_exp.html', title='new_experiment',
        form=form,legend='New Experiment',column_name=column_name,custom_clearing=custom_clearing)  

class State(object):
    def __init__(self):
        self.state='California'

@main.route("/form_autofill",methods=['GET','POST']) 
def form_autofill(): 
    # myobj = [{'grade':'A+'}]
    state_contents = db.State() & 'state="California"'
    state_dict = state_contents.fetch1()

    form = StateForm()
    for key,val in list(state_dict.items()):
        if username in form._fields.keys():
            form[key].data = val
        # print(key,val)
    return render_template('form_autofill.html', form=form)  


@main.route('/plots/breast_cancer_data/correlation_matrix', methods=['GET'])
def correlation_matrix():
    bytes_obj = do_plot()
    
    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')


@main.route('/plots/breast_cancer_data/show_correlation_matrix', methods=['GET'])
def show_correlation_matrix():
    
    return render_template('plot.html')

@main.route('/dynamic_flask_table', methods=['GET'])
def dynamic_flask_table():
    sort = request.args.get('sort', 'state') # first is the variable name, second is default value
    reverse = (request.args.get('direction', 'asc') == 'desc')
    contents = db.County()
    # print(contents.fetch('county'))
    # sorted_contents = sorted(contents.fetch(as_dict=True),
    #         key=partial(table_sorter,sort_key=sort),reverse=reverse)

    table = tables.create_dynamic_table(contents,sort_by=sort,sort_reverse=reverse)
    # print(sorted_contents)
    return render_template('dynamic_table.html',table=table)


@main.route('/flask_table_custom_border', methods=['GET'])
def flask_table_custom_border():
    sort = request.args.get('sort', 'state') # first is the variable name, second is default value
    reverse = (request.args.get('direction', 'asc') == 'desc')
    contents = db.County()
    # print(contents.fetch('county'))
    # sorted_contents = sorted(contents.fetch(as_dict=True),
    #         key=partial(table_sorter,sort_key=sort),reverse=reverse)

    table = tables.create_custom_border_table(contents,sort_by=sort,sort_reverse=reverse)
    # print(sorted_contents)
    return render_template('custom_table_border.html',table=table)    


@main.route('/flask_table_custom_columns', methods=['GET'])
def flask_table_custom_columns():
    data = [{'number_of_samples':5,"uniform_clearing":True},{'testcol':'no'},{'testcol':'maybe'}]
    # print(contents.fetch('county'))
    # sorted_contents = sorted(contents.fetch(as_dict=True),
    #         key=partial(table_sorter,sort_key=sort),reverse=reverse)
    table = tables.CustomTestTable(data)
    # print(sorted_contents)
    return render_template('custom_table_cols.html',table=table) 


@main.route('/flask_table_custom_rows', methods=['GET'])
def flask_table_custom_rows():
    test_data = [{'username':'user1','age':20,'sex':'F'},
                 {'username':'user2','age':22,'sex':'M'},
                 {'username':'user3','age':30,'sex':'F'}]
    table = tables.dynamic_table_custom_rows(test_data)
    return render_template('test_customrows.html',table=table)


@main.route('/flask_table_custom_data', methods=['GET'])
def flask_table_custom_data():
    test_data = [{'username':'user1','age':20,'sex':'F'},
                 {'username':'user2','age':22,'sex':'M'},
                 {'username':'user3','age':30,'sex':'F'}]
    table = tables.TestTableCustomCol(test_data)
    return render_template('test_customrows.html',table=table)


@main.route('/flask_table_custom_linkcol', methods=['GET'])
def flask_table_custom_linkcol():
    test_data = [{'username':'user1','age':20,'sex':'F'},
                 {'username':'user2','age':22,'sex':'M'},
                 {'username':'user3','age':30,'sex':'F'}]
    table = tables.TestTableCustomLinkCol(test_data)
    return render_template('test_customrows.html',table=table)