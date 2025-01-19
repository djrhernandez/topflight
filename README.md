# Topflight API

Topflight is a Python backend that uses a GraphQL API along with Flask, Ariadne, and Socrata.

## Installation
1. Create and establish your Python virtualenv environment on the CMD line
```bash
python3 -m venv venv;
source ./venv/bin/activate;
```

2. Then, install the dependencies
```bash
pip install -r requirements.txt
```

3. Finally, run the project
```bash
python app.py
```

## GraphQL Queries
Here are some GraphQL queries to get started. More are soon to come.
```graphql
query fetchAllHotels {
  hotels {
    parid
    borough
    owner_name
    postcode
    street_address
  }
}

query fetchHotelsNearLocation($latitude: Float!, $longitude: Float!, $radius: Float!) {
  hotelsNearLocation(latitude: $latitude, longitude: $longitude, radius: $radius) {
    parid
    owner_name
    borough
    longitude
    latitude
    postcode
    street_address
  }
}
```

Examples for Query Variables:
```graphql
{
  "borough": "Manhattan",
  "postcode": 10005,
  "latitude": 40.705187,
  "longitude": -74.006694,
  "radius": 2.0
}
```

---

## Troubleshooting
If you need to update the requirements.txt file so the app runs correctly, install and run the `pipreqs` command.
For more info, check out the documentation for [pipreqs](https://pypi.org/project/pipreqs/):
```bash
pip install pipreqs
pipreqs /path/to/app  # use --force if necessary
```