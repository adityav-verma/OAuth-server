from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import InputRequired

class RegistrationForm(FlaskForm):
    name = TextField('Name', validators=[InputRequired()])
    password = TextField('Password', validators=[InputRequired()])
