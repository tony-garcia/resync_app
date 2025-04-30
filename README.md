# Compound Data API MVP

This code provides an MVP of a CRUD API for a compound database (identified by SMILES) and associated arbitrary key-value simple data (strings, integers and floats).

## Key Components
* The `api` directory contains a [Django](https://www.djangoproject.com/) project (`compound_manager`) that implements the API using the [Django REST Framework](https://www.django-rest-framework.org/)
* Data are stored in a PostgreSQL database

## Launching the API
The application is containerized. Therefore you will need to make sure you have [docker installed](https://docs.docker.com/engine/install/) and running before spinning it up.

Once you have docker running, execute this command to spin up the API:

    docker compose up

Once the containers are running, the API is accessible at http://localhost:8000/api/

To stop the application run one of the following commands

    docker compose stop  # stops the containers
    docker compose down  # stops the containers and removes them

## API Usage

### CRUD Operations
This is an example of using the api from a python script (uses the `httpx` library). Compounds have a `smiles` property for SMILES strings, and a `data` property, which is a key-value store in which keys are strings and values can be either strings, integers, or floats.

```
import os
import httpx

BASE_URL = "http://localhost:8000/api/"

# CREATE (post)
resp = httpx.post(
    os.path.join(BASE_URL, "compounds/"),
    json={
        "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
        "data": {"name": "Caffeine", "type": "Stimulant", "classification": "OTC", "score": 75},
    },
)

# BULK CREATE
resp = httpx.post(
    os.path.join(BASE_URL, "compounds/"),
    json=[
    {
        "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
        "data": {"name": "Caffeine", "type": "Stimulant", "classification": "OTC", "score": 75},
    },
    {
        "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
        "data": {"name": "Aspirin", "type": "NSAID", "classification": "OTC", "score": 85},
    }
])

# READ (get)
resp = httpx.get(os.path.join(BASE_URL, "compounds/1/"))

print(resp.json())
{
    "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "data": {"name": "Caffeine", "type": "Stimulant", "classification": "OTC", "score": 75},
}

# UPDATE (put) -- this replaces an existing compound fully
resp = httpx.put(
    os.path.join(BASE_URL, "compounds/1/"),
    json={
        "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
        "data": {"name": "Caffeine", "type": "Stimulant", "classification": "OTC", "score": 80},
    },
)

# PARTIAL UPDATE (patch) -- this replaces only properties that are in the payload. This will remove the `classification` property in the data and update the `score`.
resp = httpx.put(
    os.path.join(BASE_URL, "compounds/1/"),
    json={"data": {"classification": "", "score": 90}},

)
# DELETE (delete)
resp = httpx.delete(os.path.join(BASE_URL, "compounds/1/"))

# LIST
resp = httpx.get(os.path.join(BASE_URL, "compounds/"))
```
### Search API
Data values can be searched using the url query param pattern `?data__{property}__{operator}={search_term}`, with `property` being the data property being searched on and the operators being:
* `eq` (equals -- for numeric or string values). This is the default and has the format `?data__{property}={search_term}
* `gt` (greater than -- for numeric values)
* `gte` (greater than or equal to -- for numeric values)
* `lt` (less than -- for numeric values)
* `lte` (less than or equal to -- for numeric values)
* `contains` (string contains search term, case insensitive)
* `startswith` (string starts with)
* `endswith` (string ends with)
* `has_key` (data has the key specified in the search term, therefore no property is specified)

For example a GET request to this url gets all compounds whose data has the classification property and whose purity is > 90

    search_results = httpx.get(os.path.join(BASE_URL, "compounds/?data__haskey=classification&data__purity__gt=90"))

For a text search accross all data properties, use the `?search={search_term}` query parameter.

    search_all_props = httpx.get(os.path.join(BASE_URL, "compounds/?search=alde"))

## Running Tests
Tests are written using pytest and are in the `api/compound_manager/tests` directory. To run them, execute the `test.sh` script, which spins up docker containers and runs the tests:

    ./test.sh

