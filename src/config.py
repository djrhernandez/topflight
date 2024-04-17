# config.py

import os

class Config:
    # BACKEND_API = "https://topflight-0e1ab3703bed.herokuapp.com/"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost/MyDB'
    SQLALCHEMY_DATABASE_URI = "sqlite:////home/path/to/app/src/skyhawk.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = "Content-Type"
    NY_API_BASE_URL = "https://data.cityofnewyork.us"
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    }
    NYC_PARAMS = {
        '$limit' : '15',
    }