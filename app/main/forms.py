from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, SelectField,
					 BooleanField, HiddenField, IntegerField, FieldList, FormField,
					 SelectMultipleField, DateField)
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError, Email, Optional 
from wtforms.widgets import html5, CheckboxInput, ListWidget

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


class CustomBusinessForm(FlaskForm):
	name = StringField('Business Name')
	number_of_days = IntegerField('Number of days the business is open',widget=html5.NumberInput(),
		validators=[InputRequired()],id='ndays')
	customize_business_hours = BooleanField('Customize your business hours?',id='customize_checkbox')
	hours = FieldList(FormField(TimeForm), min_entries=0,max_entries=7)


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class CheckboxGridForm(FlaskForm):
	# top_labels = 
    channel488 = MultiCheckboxField('488',choices=[(0,''),(1,''),(2,''),(3,'488'),
    											   (4,''),(5,''),(6,''),(7,'555'),
    											   (8,''),(9,''),(10,''),(11,'647'),
    											   (12,''),(13,''),(14,''),(15,'790')], coerce=int)

    submit = SubmitField("Set User Choices")

class GradeForm(FlaskForm):
	grade = StringField('Student grade')
	submit = SubmitField("Submit")

class WorkReportEntry(FlaskForm):
    index = HiddenField('index')
    # date = DateField('date')
    start_time = StringField('Start Start')
    end_time = StringField('Start End')
    is_entered = BooleanField('Entered already?')

class WorkReportForm(FlaskForm):
    """A form for one or more addresses"""
    days = FieldList(FormField(WorkReportEntry), min_entries=1)
    submit = SubmitField('Save')  

class ChannelForm(FlaskForm):
	channel = SelectField('channel',choices=[('488','488'),('555','555'),
    	('647','647'),('790','790')])	
	registration = BooleanField('Registration',default=False)
	injection_detection = BooleanField('Injection detection',default=False)
	probe_detection = BooleanField('Injection detection',default=False)
	cell_detection = BooleanField('Injection detection',default=False)

class ChannelListForm(FlaskForm):
	"""A form for picking which channels were used for what purpose"""
	# channels = FieldList(FormField(ChannelForm), min_entries=4,max_entries=4)
	channel1_registration = BooleanField('Registration',default=False)
	channel1_injection_detection = BooleanField('Registration',default=False)
	channel1_probe_detection = BooleanField('Registration',default=False)
	channel1_cell_detection = BooleanField('Registration',default=False)
	channel2_registration = BooleanField('Registration',default=False)
	channel2_injection_detection = BooleanField('Registration',default=False)
	channel2_probe_detection = BooleanField('Registration',default=False)
	channel2_cell_detection = BooleanField('Registration',default=False)

	submit = SubmitField('Save')  



