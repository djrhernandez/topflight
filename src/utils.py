# utils.py
import os
import requests
from sqlalchemy import Null
from math import radians, sin, cos, sqrt, atan2
from src.graphql import app

from .config import Config

def create_db_path(name, base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(base_dir, name)
    full_path = "sqlite:///" + db_path
    if not os.path.isdir(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    return full_path


def list_public_attributes(obj):
    # Filter out magic methods and sort
    attributes = [attr for attr in dir(obj) if not attr.startswith('__')]
    attributes.sort()   # Sorting the attributes for better readability
    return attributes


def print_public_attributes(obj):
    attributes = list_public_attributes(obj)
    for idx, attr in enumerate(attributes, start=1):
        print(f"{idx}: {attr}")


# Haversine Formula: 
# Meant to calculate the distance between 2 geographic coordinates based on Earth's curvature
# Steps: 
# 1. Convert latitude and longitude from degrees to radians
# 2. Apply the Haversine function to compute the great-circle distance between the 2 pts
#       - Sum = square of sine of half the lat diff + Earth's curvature using lat/long diffs
# 3. Find the central angle using the arctangent function:
#       - Return the angle whose tangent is the quotient of two specified numbers5
# 4. Return the distance btwn the two points using the radius of Earth
def calculate_distance(lat1, long1, lat2, long2):
    lat_diff = radians(lat2 - lat1)
    long_diff = radians(long2 - long1)
    
    a = sin(lat_diff / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(long_diff / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    R = 3958.8  # Radius of the Earth in miles
    return R * c


def get_borough(hotel_data, borocode):
    borough = hotel_data.get('borough', 'Unknown').title()
    if borough in ['Unknown', 'Staten Is'] and borocode != Null:
        borough = Config.BOROUGH_MAP.get(borocode, 'Unknown')
    return borough


def create_hotel_record(hotel_data, models):
    street_address = f"{hotel_data.get('street_num', '')} {hotel_data.get('street_name', '')}"
    
    return models.Hotel(
        parid = int(hotel_data.get('parid', 0)),
        bbl = int(hotel_data.get('bbl', 0)),
        bldg_class = hotel_data.get('bldg_class', ''),
        bldg_id_number = int(hotel_data.get('bin', 0)),
        block = int(hotel_data.get('block', 0)),
        borocode = int(hotel_data.get('borocode', 0)),
        borough = get_borough(hotel_data, hotel_data.get('borocode', 0)),
        census_tract = int(hotel_data.get('census_tract', 0)),
        community_board = int(hotel_data.get('community_board', 0)),
        council_district = int(hotel_data.get('council_district', 0)),
        latitude = float(hotel_data.get('latitude', 0.0)),
        longitude = float(hotel_data.get('longitude', 0.0)),
        lot = int(hotel_data.get('lot', 0)),
        nta_name = hotel_data.get('nta', ''),
        nta_code = hotel_data.get('nta_code2', ''),
        owner_name = hotel_data.get('owner_name', ''),
        postcode = int(hotel_data.get('postcode', 0)),
        street_address = street_address,
        tax_class = hotel_data.get('taxclass', ''),
        tax_year = int(hotel_data.get('taxyear', ''))
    )


def process_and_store_hotel_data(data, db, models):
    parids = [int(hotel_data.get('parid', 0)) for hotel_data in data]
    existing_hotels = {hotel.parid: hotel for hotel in models.Hotel.query.filter(models.Hotel.parid.in_(parids)).all()}
    
    new_hotels = []
    for hotel_data in data:
        parid = int(hotel_data.get('parid', 0))
        if parid not in existing_hotels:
            hotel = create_hotel_record(hotel_data, models)
            new_hotels.append(hotel)
    
    if new_hotels:
        db.session.bulk_save_objects(new_hotels)
        db.session.commit()


def backup_fetch_nyc_data():
    try:
        response = requests.get(Config.NYC_API_BASE_URL + '/resource/tjus-cn27.json', headers=Config.HEADERS, params=Config.NYC_PARAMS)
        if response.status_code == 200:
            data = response.json()
            app.logger.info(f"Successfully fetched {len(data)} records.")
            return data
        else:
            app.logger.error(f"Failed to fetch data. Status code: {response.status_code}")
            app.logger.error(f"Error message: {response.text}")
            return None
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return None