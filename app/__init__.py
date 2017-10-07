from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider
import settings

app = Flask(__name__)
app.config.from_object('app.settings')

db = SQLAlchemy(app)

oauth = OAuth2Provider(app)
from app.oauth_helpers import *

from app.models import *
from app.views import *
