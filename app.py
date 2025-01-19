# app.py
from flask_cors import CORS

import atexit
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.interval import IntervalTrigger
from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers
from sodapy import Socrata
from sqlalchemy import inspect

from src.config import Config
from src.routes import init_app
from src.graphql import app, db, models, queries
from src.utils import process_and_store_hotel_data, backup_fetch_nyc_data

# Basic logging for App and Scheduler
logging.basicConfig(level=logging.INFO)
logging.getLogger('apscheduler').setLevel(logging.INFO)

# Make sure schema is defined
type_defs = load_schema_from_path("src/graphql/schema.graphql")
schema = make_executable_schema(type_defs, [queries.query, snake_case_fallback_resolvers])

CORS(app, resources={r"/graphql": {"origins": Config.CORS_ORIGINS}})

# Unauth client only works with public data sets.
# URL to use the auth client: https://dev.socrata.com/foundry/data.cityofnewyork.us/tjus-cn27
app_token = Config.NYC_API_TOPFLIGHT_APP_TOKEN
soc_client = Socrata(Config.NYC_API_BASE_URL, app_token, timeout = 30)
if soc_client:
    app.logger.info(
        "Socrata client created - URI Prefix: '{uri_prefix:}' | Domain: '{domain:}' | Session: {session:} | APP Token: {app_token}"
        .format(**soc_client.__dict__, app_token = app_token)
    )
else:
    app.logger.error("Failed to create Socrata client. Exiting.")
    exit(1)


def fetch_nyc_data():
    with app.app_context():
        try:
            response = soc_client.get("tjus-cn27", limit=2)
            if not response:
                app.logger.warning("No data returned from NYC API.\n")
                return False

            process_and_store_hotel_data(response, db, models)
            app.logger.info("NYC data loaded into the database.\n")
        
        except SystemError as err:
            app.logger.error(f"SystemError - fetch_nyc_data(): {err}\n")
            return False
        except Exception as err:
            app.logger.error(f"Exception - fetch_nyc_data(): {err}\n")
            return False
        except BaseException as err:
            app.logger.error(f"BaseException - fetch_nyc_data(): {err}\n")
            return False
        
        app.logger.info("Fetching NYC data done.\n")
        return True


def initialize_db():
    with app.app_context():
        db_inspect = inspect(db.engine)
        
        if not db_inspect.has_table("hotel"):
            app.logger.info("Hotel table does not exist. Creating table...")
            db.create_all()
            
            app.logger.info("Fetching data from NYC API...")
            data_fetched = fetch_nyc_data()
            if not data_fetched:
                app.logger.error("Failed to fetch data from NYC API. Retrying from backup protocols...")
                
                backup_fetched = backup_fetch_nyc_data()
                if not backup_fetched:
                    app.logger.error("Failed to refetch data from backup protocols. Exiting..")
                    exit(1)
                else:
                    process_and_store_hotel_data(backup_fetched, db, models)
        else:
            app.logger.info("Hotel table already exists.")


def start_scheduler():
    # Set jobstore for scheduled API fetching
    jobstores = { 'default': SQLAlchemyJobStore(url=Config.SQLALCHEMY_DATABASE_URI) }
    
    scheduler = BackgroundScheduler(jobstores=jobstores)
    scheduler.start()
    
    if not scheduler.get_job('fetch_nyc_data'):
        app.logger.info("Adding new job: fetch_nyc_data")
        scheduler.add_job(
            func=fetch_nyc_data,
            trigger=IntervalTrigger(days=3),
            next_run_time=datetime.now() + timedelta(seconds=1),
            id='fetch_nyc_data',
            name='Fetch NYC OpenData Hotel Info Every 3 Days',
            replace_existing=True
        )
    
    # Shut down scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown(wait=False))


# Initialize app and database
init_app(app, schema, soc_client, db)

if __name__ == '__main__':
    initialize_db()
    start_scheduler()
    app.run(debug=True)