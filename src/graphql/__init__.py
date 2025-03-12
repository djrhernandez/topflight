from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from src.config import Config

app = Flask(__name__)

CORS(app, 
    resources=r"/*", 
    origins=['http://localhost:3000', 'https://skyhawk.vercel.app'],
    supports_credentials=True,
)

app.config.from_object(Config)
app.app_context().push()
db = SQLAlchemy(app)