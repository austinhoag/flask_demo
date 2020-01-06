from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, SelectField,
					 BooleanField, HiddenField, IntegerField, FieldList, FormField,
					 SelectMultipleField)
from wtforms import DateField as OGDateField
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError, Email, Optional 
from wtforms.widgets import html5, CheckboxInput, ListWidget
from wtforms.fields.html5 import DateField, DateTimeLocalField
# from wtforms.fields.html5 import DateTimeLocalField


datetimeformat='%Y-%m-%dT%H:%M' # To get form.field.data to work. Does not work with the default (bug)

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
	grade1 = StringField('Student 1 grade')
	grade2 = StringField('Student 2 grade')
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

def OptionalDateField(description='',validators=[],format=''):
	""" A custom field that makes the DateField optional """
	validators.append(Optional())
	field = DateField(description,validators,format=format)
	return field

class ClearingForm(FlaskForm):
	""" The form for clearing a single sample within an experiment """
	# Basic info
	clearing_protocol = SelectField('Clearing Protocol:', choices= \
		[('iDISCO abbreviated clearing','iDISCO for non-oxidizable fluorophores (abbreviated clearing)'),
		 ('iDISCO abbreviated clearing (rat)','Rat: iDISCO for non-oxidizable fluorophores (abbreviated clearing)'),
	     ('iDISCO+_immuno','iDISCO+ (immunostaining)'),
	     ('uDISCO','uDISCO'),('iDISCO_EdU','Wang Lab iDISCO Protocol-EdU')],validators=[InputRequired()]) 
	antibody1 = TextAreaField('Primary antibody and concentrations desired (if doing immunostaining)',validators=[Length(max=100)])
	antibody2 = TextAreaField('Secondary antibody and concentrations desired (if doing immunostaining)',validators=[Length(max=100)])
	perfusion_date = OptionalDateField('Perfusion Date (leave blank if unsure):')
	expected_handoff_date = OptionalDateField('Expected date of hand-off (leave blank if not applicable or unsure):')

	def validate_antibody1(self,antibody1):
		''' Makes sure that primary antibody is not blank if immunostaining clearing protocol
		is chosen  '''
		if self.clearing_protocol.data == 'iDISCO+_immuno' and antibody1.data == '':
			raise ValidationError('Antibody must be specified because you selected \
				an immunostaining clearing protocol')

class ImagingForm(FlaskForm):
	""" The form for imaging a single sample within an experiment """
	# Basic info
	image_resolution = SelectField('Image Resolution:', 
		choices=[('1.3x','1.3x (low-res: good for site detection, whole brain c-fos quantification, or registration)'),
	('4x','4x (high-res: good for tracing, cell detection)')],validators=[InputRequired()]) # for choices first element of tuple is the value of the option, the second is the displayed text
	channel488_registration = BooleanField('Registration',default=False)
	channel488_injection_detection = BooleanField('Registration',default=False)
	channel488_probe_detection = BooleanField('Registration',default=False)
	channel488_cell_detection = BooleanField('Registration',default=False)
	channel555_registration = BooleanField('Registration',default=False)
	channel555_injection_detection = BooleanField('Registration',default=False)
	channel555_probe_detection = BooleanField('Registration',default=False)
	channel555_cell_detection = BooleanField('Registration',default=False)
	channel647_registration = BooleanField('Registration',default=False)
	channel647_injection_detection = BooleanField('Registration',default=False)
	channel647_probe_detection = BooleanField('Registration',default=False)
	channel647_cell_detection = BooleanField('Registration',default=False)
	channel790_registration = BooleanField('Registration',default=False)
	channel790_injection_detection = BooleanField('Registration',default=False)
	channel790_probe_detection = BooleanField('Registration',default=False)
	channel790_cell_detection = BooleanField('Registration',default=False)


class ExpForm(FlaskForm):
	""" The form for requesting a new experiment/dataset """
	# Basic info
	# title = StringField('Title of experiment',validators=[InputRequired(),Length(max=100)])
	# description = TextAreaField('Description of experiment',validators=[InputRequired(),Length(max=250)])
	# labname = StringField('Lab name(s) (e.g. Tank/Brody)',validators=[InputRequired(),Length(max=100)])
	# correspondence_email = StringField('Correspondence email (default is princeton email)',
		# validators=[DataRequired(),Length(max=100),Email()])

	# species = SelectField('Species:', choices=[('mouse','mouse'),('rat','rat'),('primate','primate'),('marsupial','marsupial')],validators=[InputRequired(),Length(max=50)]) # for choices first element of tuple is the value of the option, the second is the displayed text
	number_of_samples = IntegerField('Number of samples (a.k.a. tubes)',widget=html5.NumberInput(),validators=[InputRequired()])
	sample_prefix = StringField('Sample prefix (your samples will be named prefix-1, prefix-2, ...)',validators=[InputRequired(),Length(max=32)])

	self_clearing = BooleanField('Check if you plan to do the clearing yourself',default=False)
	clearing_samples = FieldList(FormField(ClearingForm),min_entries=0,max_entries=15)
	# custom_clearing = IntegerField('Is clearing custom?',default=0)
	uniform_clearing_submit = SubmitField('Yes') # The answer to "will your clearing be the same for all samples?"	
	custom_clearing_submit = SubmitField('No') # The answer to "will your clearing be the same for all samples?"

	self_imaging = BooleanField('Check if you plan to do the imaging yourself',default=False)

	imaging_samples = FieldList(FormField(ImagingForm),min_entries=0,max_entries=15)
	# custom_imaging = IntegerField('Is imaging custom?',default=0)
	uniform_imaging_submit = SubmitField('Yes') # The answer to "will your imaging be the same for all samples?"	
	custom_imaging_submit = SubmitField('No') # The answer to "will your imaging be the same for all samples?"

	submit = SubmitField('Submit request')	

	def validate_clearing_samples(self,clearing_samples):
		""" Make sure that user has answered the question of 
		whether to use unique clearing before being able to submit the whole form
		""" 
		if self.submit.data == True:
			if len(clearing_samples.data) == 0 and not (self.uniform_clearing_submit.data == True or self.custom_clearing_submit == True):
				raise ValidationError("Please answer the question in the Clearing Info section first.")

	def validate_imaging_samples(self,imaging_samples):
		""" Make sure that user has answered the question of 
		whether to use unique clearing before being able to submit the whole form
		""" 
		if self.submit.data == True:
			if len(imaging_samples.data) == 0 and not (self.uniform_imaging_submit.data == True or self.custom_imaging_submit == True):
				raise ValidationError("Please answer the question in the Imaging/Processing Info section first.")


class StateForm(FlaskForm):
	state = StringField('State')
	submit = SubmitField('Submit request')


def OptionalDateTimeLocalField(description='',validators=[],format=datetimeformat):
	""" A custom field that makes the DateTimeLocalField optional
	and applies a specific formatting to fix a bug in the default formatting """
	validators.append(Optional())
	field = DateTimeLocalField(description,validators,format=format)
	return field

class DateTimeForm(FlaskForm):
	""" The form for entering clearing information """
	
	datetime1 = OptionalDateTimeLocalField('Datetime 1')
	datetime2 = OptionalDateTimeLocalField('Datetime 2')
	submit = SubmitField("Submit")


class SimpleDateForm(FlaskForm):
	""" The form for clearing a single sample within an experiment """
	# Basic info
	name = StringField('name')
	date1 = StringField('Date1',validators=[Optional()])
	date2 = StringField('Date2',validators=[Optional()])
	submit = SubmitField("Submit")
