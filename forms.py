from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('Search')

class EditForm(FlaskForm):

    fname = StringField('First Name:', validators=[DataRequired()])
    lname = StringField('Last Name:', validators=[DataRequired()])
    footsize = IntegerField('Footsize:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewUserForm(FlaskForm):

    fname = StringField('First Name:', validators=[DataRequired()])
    lname = StringField('Last Name:', validators=[DataRequired()])
    footsize = IntegerField('Footsize:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Submit')

