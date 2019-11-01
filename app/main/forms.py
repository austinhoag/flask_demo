from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, SelectField,
					 BooleanField, HiddenField, IntegerField, FieldList, FormField)
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError, Email, Optional 
from wtforms.widgets import html5

# from lightserv.models import Experiment

class SvgForm(FlaskForm):
	""" The form for requesting a new experiment/dataset """

	# Basic info

	species = SelectField('Species:', 
		choices=[('mouse','mouse'),('rat','rat'),
				 ('primate','primate'),('marsupial','marsupial')],
				 validators=[InputRequired()])


class PickCounty(FlaskForm):
	# form_name = HiddenField('Form Name')
	state = SelectField('State:', choices=[],validators=[InputRequired()],id='select_state') # id used to access in javascript
	county = SelectField('County:', validators=[DataRequired()],id='select_county')

	submit = SubmitField('Select County!')


class ExperimentForm(FlaskForm):
	# form_name = HiddenField('Form Name')
	title = StringField('Title of experiment:',validators=[InputRequired()]) # id used to access in javascript
	number_of_samples = IntegerField('Number of samples',widget=html5.NumberInput(),validators=[InputRequired()],id='nsamples')
	customize_sample_names = BooleanField('Customize your sample names?',id='customize_checkbox')
	submit = SubmitField('Submit')	


class TimeForm(FlaskForm):
    opening = StringField('Opening Hour')
    closing = StringField('Closing Hour')
    day = HiddenField('Day')

class BusinessForm(FlaskForm):
    name = StringField('Business Name')
    hours = FieldList(FormField(TimeForm), min_entries=0,max_entries=7)

class CustomTimeForm(FlaskForm):
    opening = StringField('Opening Hour')
    closing = StringField('Closing Hour')
    day = HiddenField('Day')

class CustomBusinessForm(FlaskForm):
	name = StringField('Business Name')
	number_of_days = IntegerField('Number of days the business is open',widget=html5.NumberInput(),
		validators=[InputRequired()],id='ndays')
	customize_business_hours = BooleanField('Customize your business hours?',id='customize_checkbox')
	hours = FieldList(FormField(TimeForm), min_entries=0,max_entries=7)