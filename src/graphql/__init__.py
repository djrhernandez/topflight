from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.app_context().push()
db = SQLAlchemy(app)