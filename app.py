# app.py

from flask import Flask, jsonify, request
from flask_graphql import GraphQLView

from sodapy import Socrata

import urllib.parse as up
from urllib.parse import urlencode

from src.config import Config
from src.schema import schema
from src.models import db_session, Hotels, Owners

import logging
logging.basicConfig(level=logging.INFO)

# Unauth client only works with public data sets.
# Visit the URL to use the auth client:
# https://dev.socrata.com/foundry/data.cityofnewyork.us/tjus-cn27
client = Socrata(Config.NYC_API_BASE_URL, None)

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func = GraphQLView.as_view(
        'graphql',
        schema = schema,
        graphiql = True, # for having the GraphiQL interface
        default_query = Config.GRAPHQL_QUERY
    )
)


def fetch_nyc_data():
    limits = Config.NYC_DATA_LIMIT

    try:
        response = client.get("tjus-cn27", limit=limits)
        if not response:
            logging.info("No data present in response.")
            return []

        for item in response:
            existing_hotel = db_session.query(Hotels).filter_by(parid=item.get("parid")).first()
            existing_owner = db_session.query(Owners).filter_by(id=item.get("id")).first()

            if not existing_hotel:
                hotel = Hotels(**item)
                db_session.add(hotel)
            else:
                logging.info(f"Entry already exists for Hotel ID: {item.get('parid')}")

            if not existing_owner:
                owner = Owners(
                    name = item.get('owner_name')
                )
                db_session.add(owner)
            else:
                logging.info(f"Entry already exists for Owner ID: {item.get('id')}")

        db_session.commit()
        return response
    except Exception as err:
        db_session.rollback()
        logging.error(f"Failed to fetch data: {err}", exc_info=True)
        return {"message": f"Failed to fetch data: {str(err)}"}
    finally:
        db_session.close()


with app.app_context():
    fetch_nyc_data()


@app.route('/')
def health_check():
    return "OK"


@app.route('/nyc_data', methods=["GET"])
def check_nyc():
    try:
        response = fetch_nyc_data()

        if response:
            return jsonify({"message": "Data fetched successfully.", "data": response}), 200
        else:
            return jsonify({"message": "Failed to fetch data from NYC URL with given parameters.", "data": []}), 401
    except Exception as err:
        return jsonify({"message": "Error fetching data.", "error": str(err)}), 500


@app.teardown_appcontext
def teardown_db(Exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()