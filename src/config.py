import os
from dotenv import load_dotenv
from src.yaml_loader import load_yaml_files

# Load .env file
load_dotenv()

# Base directory path for SQLite or other local files
basedir = os.path.abspath(os.path.dirname(__file__))

# The Directory YAML configuration files are stored
YAML_CONFIG_DIR = os.path.join(basedir, "./yaml_files")

# Load the YAML files on startup
yaml_configs = load_yaml_files(YAML_CONFIG_DIR)

class Config:
    BOROUGH_MAP = {
        0: 'Unknown',
        1: 'Manhattan',
        2: 'Bronx',
        3: 'Brooklyn',
        4: 'Queens',
        5: 'Staten Island'
    }
    CORS_ORIGINS = {
        'origin': os.environ.get("CORS_ORIGINS"),
        'methods': '*',
        'allow_headers': '*',
    }
    DEBUG = True
    ENV = os.environ.get('ENV')  # Defaulting to production for obvious reasons
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "X-App-Token": os.environ.get("NYCOD_API_TOPFLIGHT_APP_TOKEN")
    }
    GRAPHQL_QUERY = '''
    query fetchAllHotels {
        hotels {
            parid
            bbl  
            bldg_class
            bldg_id_number
            block
            borocode
            borough
            census_tract
            community_board
            council_district
            latitude
            longitude
            lot
            nta_code
            nta_name
            owner_name
            postcode
            street_address
            tax_class
            tax_year
        }
    }
    '''
    NYCOD_API_BASE_URL = os.environ.get("NYCOD_API_BASE_URL")
    NYCOD_API_DATA_LIMIT = int(os.environ.get("NYCOD_API_DATA_LIMIT", 20000 if ENV == "production" else 200))
    NYCOD_API_USERNAME = os.environ.get("NYCOD_API_USERNAME")
    NYCOD_API_PASSWORD = os.environ.get("NYCOD_API_PASSWORD")
    
    NYCOD_API_KEY_ID = os.environ.get("NYCOD_API_TF_KEY_ID")
    NYCOD_API_SECRET_KEY = os.environ.get("NYCOD_API_TF_SECRET_KEY")
    NYCOD_API_TOPFLIGHT_APP_TOKEN = os.environ.get("NYCOD_API_TF_APP_TOKEN")
    NYCOD_API_TOPFLIGHT_APP_TOKEN_SECRET = os.environ.get("NYCOD_API_TF_APP_TOKEN_SECRET")
    
    OPENAI_KEY = os.environ.get("OPENAI_KEY")
    
    NYCOD_PARAMS = {
        "$limit": NYCOD_API_DATA_LIMIT,
    }
    
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
    SKYHAWK_URL = os.environ.get("SKYHAWK_DOMAIN_URL")
    
    STEAM_WEB_API_BASE_URL = os.environ.get("STEAM_WEB_API_BASE_URL")
    STEAM_WEB_API_KEY = os.environ.get("STEAM_WEB_API_KEY")
    STEAM_WEB_DOMAIN_NAME = os.environ.get("STEAM_WEB_DOMAIN_NAME")
    
    # Database URI
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "database/skyhawk.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    VIEW_MODE = os.environ.get('VIEW_MODE')
    
    YAML_DATA = yaml_configs
    YAML_DATA_APP_SETTINGS = YAML_DATA.get('app_config', {}).get('app_settings', {})
    YAML_NYC_CONFIG_DATA = YAML_DATA.get('nyc_config', {}).get('nyc_data', {})
