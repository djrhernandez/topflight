from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from src.config import Config

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config.from_object(Config)
app.app_context().push()
db = SQLAlchemy(app)