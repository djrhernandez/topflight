# app.py

from flask import Flask, jsonify, request
from flask_graphql import GraphQLView

# import pandas as pd   # uncomment to use Pandas
from sodapy import Socrata

import urllib.parse as up
from urllib.parse import urlencode

from src.config import Config
from src.schema import schema
from src.models import db_session, Hotels


# Start client for NYC data.
# NOTE: Unauth client only works with public data sets. Note 'None'
# in place of application token, and no username or password.
# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cityofnewyork.us, MyAppToken, username="user@example.com", password="SomePassword")
client = Socrata("data.cityofnewyork.us", None)

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)


def fetch_nyc_data(params):
    limits = params["$limit"]

    try:
        # NOTE: If you decide to use Panda module, you must remove the code
        # below, uncomment the module and add this snippet:
        # Convert to pandas DataFrame
        # results = pd.DataFrame.from_records(response)
        
        # Client returns JSON results from the API.
        # Converts to Python list of dictionaries with sodapy.
        response = client.get("tjus-cn27", limit=limits)

        if response:
            if response:
                for item in response:
                    if item:
                        existing_hotel = db_session.query(Hotels).filter_by(parid=item.get("parid")).first()

                        if not existing_hotel:
                            hotel = Hotels(**item) # pass all kv pairs as arguments for entry
                            db_session.add(hotel)
                        else:
                            print(f"Entry already exists for Hotel ID: {item.get('parid')}")

                db_session.commit()
            else:
                print(f"No data present => response: {response}")

            return response
    except Exception as err:
        return {"message": f"Failed to fetch data => str({err})\n"}


@app.route('/nyc_data', methods=["GET"])
def check_nyc():
    params = request.args
    if not params:
        params = Config.NYC_PARAMS

    try:
        response = fetch_nyc_data(params)

        if response:
            return jsonify({"message": "Data fetched successfully.", "data": response}), 200
        else:
            return jsonify({"message": "Failed to fetch data from NYC URL with given parameters.", "data": []}), 401
    except Exception as err:
        return jsonify({"message": "Error fetching data.", "error": str(err)}), 500


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()