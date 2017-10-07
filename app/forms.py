from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import InputRequired

class RegistrationForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired()])
    password = TextField('Password', validators=[InputRequired()])
