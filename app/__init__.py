from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import settings

app = Flask(__name__)
app.config.from_object('app.settings')

db = SQLAlchemy(app)

from app.models import User
from app.views import *
