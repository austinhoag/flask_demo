from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError, Email, Optional 

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