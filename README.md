# Contractor manager API

## Capstone Project for Udacity's Full Stack Web Developer Nanodegree
This app will help an electrical contracting company manage their personnel and jobs. The purpose of the project is to demonstrate the skills learned in the Udacity Full Stack Nano Degree program.

Heroku Link:

Local browser address: http//:localhost:5000

## Getting Started

### Installing Dependencies

#### Python 3.7
Follow the instructions to install the latest version of python for your platform from the [python documentation](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment
For Python projects, it is recommended that you work within a virtual environment as this will keep the dependencies separate and organised for all your projects. Refer to the Python documentation on how to create a virtual environment.

####Pip Dependencies

Once you have your virtual environment setup and running, you can install the other dependencies by running:

'''bash
pip install -r requirements.txt
'''

This will install all of the required packages.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
If you do not have PostgrSQL installed, install this first (https://www.postgresql.org/download/). From within the
With Postgres running, first create the database 'capstone' by running 'postgres=# create database capstone;',

## Authentication

This application uses authentication supplied by Auth0. An [Auth0](https://auth0.com/) account will need to be created.
This application requires authentication to perform various actions. All the endpoints require various permissions, except for the root (health) endpoint. These permissions are passed to the API using bearer tokens.

You will need to create a regular web application, noting the following:
- Domain
- Client ID
- Client Secret
These parameters are needed for proper setup of the application.  

Within this account, you will need to create an API with RBAC enabled. Two Roles will also be needed:

Employee

'''bash permissions:
        get:anything
        post:anything
        '''

Manager

'''bash permissions:
        get:anything
        post:anything
        patch:anything
        delete:anything
        '''

Note the identifier, as this is needed in the setup of the application.


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_DEBUG=true
flask run
```

Setting the `FLASK_DEBUG` variable to `true` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application.

## Api documentation

## Getting Started

Base URL: This application can be run locally. The hosted version is at ''' bash somelink '''

## Endpoints and Error Handlers

#### Endpoints

1. GET     '/'
2. GET     '/contractors'
3. GET     '/contractors/int:contractor_id'
4. GET     '/clients'
5. GET     '/clients/int:client_id'
6. GET     '/jobs'
7. GET     '/jobs/int:job_id'
8. POST    '/contractors'
9. POST    '/clients'
10. POST   '/jobs'
11. PATCH  '/contractor/int:contractor_id'
12. PATCH  '/clients/int:client_id'
13. PATCH  '/jobs/int:job_id'
14. DELETE '/contractors/int:contractor_id'
15. DELETE '/clients/int:client_id'
16. DELETE '/jobs/int:job_id'

'''bash

GET '/'
- No Authorisation required
- Shows the application is running
- Does not take any arguments
- Returns:
{
    'health': "Running!!"
}

GET '/contractors'
- Requires permission: 'get:anything'
- Gets all the contractors listed in the database.
- Does not take any arguments.
- Returns:
{
    "contractors": [
        {
            "id": 4,
            "name": "Pietie Coetzee",
            "phone": "0763814921"
        },
        {
            "id": 3,
            "name": "Bertie van Rensburg",
            "phone": "0798242499"
        },

    ],
    "success": true
}


GET '/contractors/int:contractor_id'
- Requires permission: 'get:anything'
- Gets all the info from a selected contractor.
- <int:contractor_id> Replaces the ID of the contractor.
- Returns:
 {
    "contractor": {
        "id": 4,
        "name": "Pietie Coetzee",
        "phone": "0763814921"
    },
    "success": true
}

GET '/clients'
- Requires permission: 'get:anything'
- Gets all the clients listed in the database.
- Does not take any arguments.
- Returns:
{
    "clients": [
        {
            "address": "3 William Nickel",
            "id": 3,
            "name": "PIA",
            "phone": "0109293810"
        },
        {
            "address": "4 William Nickel",
            "id": 4,
            "name": "CHLOE",
            "phone": "0109293811"
        }
    ],
    "success": true
}


GET '/clients/int:client_id'
- Requires permission: 'get:anything'
- Gets all the info from a selected client.
- <int:client_id> Replaces the ID of the client.
- Returns:
{
   "client": {
       "address": "4 William Nickel",
       "id": 4,
       "name": "CHLOE",
       "phone": "0109293811"
   },
   "success": true
}

GET '/jobs'
- Requires permission: 'get:anything'
- Gets all the jobs listed in the database.
- Does not take any arguments.
- Returns:
{
    "jobs": [
        {
            "client id": 3,
            "contractor id": 3,
            "id": 3,
            "start time": "Fri, 27 Nov 2020 11:25:00 GMT"
        },
        {
            "client id": 3,
            "contractor id": 3,
            "id": 12,
            "start time": "Sun, 29 Nov 2020 12:30:00 GMT"
        }
    ],
    "success": true
}


GET '/jobs/int:job_id'
- Requires permission: 'get:anything'
- Gets all the info from a selected job.
- <int:job_id> Replaces the ID of the job.
- Returns:
{
    "job": [
        {
            "client id": 3,
            "contractor id": 3,
            "id": 3,
            "start time": "Fri, 27 Nov 2020 11:25:00 GMT"
        }
    ],
    "success": true
}

POST '/contractors'
- Requires permission: 'post:anything'
- Posts a new contractor in the database with id <int:contractor_id>
- Required input (data type):
{
  "name": (string),
  "phone": (string)
}

Returns:
{
    "added": 7, (this is the id of the new contractor)
    "success": true
}

POST '/clients'
- Requires permission: 'post:anything'
- Posts a new client in the database with id <int:client_id>
- Required input (data type):
{
  "name": (string),
  "address": (string),
  "phone": (string)
}

Returns:
{
    "added": 7, (this is the id of the new client)
    "success": true
}

POST '/jobs'
- Requires permission: 'post:anything'
- Posts a new job in the database with id <int:job_id>
- Required input (data type):

    "contractor id": (integer),
    "client id": (integer),
    "start time": (datetime)
}

Returns:
{
    "job": 7, (this is the id of the new job)
    "success": true
}

PATCH  '/contractor/int:contractor_id'
- Requires permission: 'patch:anything'
- A manager (role) can edit the details of a contractor.
- Required input (data type). Only the fields that require editing can be included
{
  "name": (string)
}

Returns:
{
    "contractor": 7, (this is the id of the edited contractor)
    "success": true
}

PATCH  '/clients/int:client_id'
- Requires permission: 'patch:anything'
- A manager (role) can edit the details of a client.
- Required input (data type). Only the fields that require editing can be included
{
  "name": (string)
}

Returns:
{
    "client": 7, (this is the id of the edited client)
    "success": true
}

PATCH  '/jobs/int:job_id'
- Requires permission: 'patch:anything'
- A manager (role) can edit the details of a job.
- Required input (data type). Only the fields that require editing can be included
{
  "contractor id": (integer)
}

Returns:
{
    "job": 7, (this is the id of the edited job)
    "success": true
}

DELETE '/contractors/int:contractor_id'
- Requires permission: 'delete:anything'
- A manager (role) can delete a contractor.
- <int:contractor_id> Replaces the ID of the contractor.
- Returns:
{
  "success": true,
  "contractor": (contractor id as an integer)
}

DELETE '/clients/int:client_id'
- Requires permission: 'delete:anything'
- A manager (role) can delete a client.
- <int:client_id> Replaces the ID of the client.
- Returns:
{
  "success": true,
  "client": (client id as an integer)
}

DELETE '/jobs/int:job_id'
- Requires permission: 'delete:anything'
- A manager (role) can delete a job.
- <int:job_id> Replaces the ID of the job.
- Returns:
{
  "success": true,
  "job": (job id as an integer)
}

'''
