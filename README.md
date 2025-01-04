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
flask --app app.py run
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

query fetchHotels($borough: [String]) {
  hotel(borough: $borough) {
    parid
    block
    borough
    latitude
    longitude
    lot
    nta
    owner_name
    street_adress
	}
}
```

In Query Variables
```graphql
{
  "borough": "MANHATTAN"
  "postcode": "10005"
}
```