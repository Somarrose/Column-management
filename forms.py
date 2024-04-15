from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')

class ColumnInfoForm(FlaskForm):
    sn = StringField('Serial Number', validators=[DataRequired(), Length(max=50)])
    supplier = StringField('Supplier', validators=[DataRequired(), Length(max=100)])
    dimension = StringField('Dimension', validators=[DataRequired(), Length(max=100)])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UsageEntryForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    column_id = SelectField('Column', coerce=int, validators=[DataRequired()])
    project = StringField('Project', validators=[DataRequired(), Length(max=100)])
    technique = StringField('Technique', validators=[DataRequired(), Length(max=100)])
    mobile_phase_a = StringField('Mobile Phase A', validators=[DataRequired(), Length(max=100)])
    mobile_phase_b = StringField('Mobile Phase B', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')
