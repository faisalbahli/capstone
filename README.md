# FSND Capstone Project

## URL

https://capstone-final-0.herokuapp.com/

### dependencies 
- Python 3.7 - Follow instructions to install the latest version of python for your platform in the python docs

- Virtual Enviornment - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

PIP Dependencies - Once you have your virtual environment setup and running, install dependencies by running the below command. This will install all of the required packages we selected within the requirements.txt file:
`pip install -r requirements.txt`


The server can be started by running the following commands:
```
set FLASK_APP=app
set FLASK_ENV=development
set FLASK_DEBUG=True
flask run
```


#### Key Dependencies

- Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

## documentation

### APP with authoization only works with Postman
This is endpoint below will redirect you sign in page by Auth0. with the previously created accounts (check Roles And Accounts section), you can sign to get authorized and get the access token from the URL to test it with Postman.


Authoirzation URL:
- `authorization/url` (GET)

It will return access token from the URL which can be used in postman to access other endpoints.


## Roles And Accounts

There are two created accounts assigned with two roles in this project:

### Manager (Authorized to all actions and endpoints)

- Email : barista.role@gmail.com
- Password: Capstone@1

Permissions for Manager:

- `delete:drinks` Remove drinks
- `get:drinks-detail` Get details about drink
- `patch:drinks` Modify drinks
- `post:drinks` Create new drink
- `post:menu` Create new menu

Authorized endpoint:

- All Endpoints


### Barista (Authorized to only GET /drinks-detail endpoint)

- Email : barista.role@gmail.com
- Password: Capstone@1

Permissions for Barista:

- `get:drinks-detail` Get details about drink

Authorized endpoint:

- `/drinks-detail`



## Endpoints
The following endpoints are in the app:

- `authorization/url` (GET)

- `/drinks` (GET)
- `/drinks` (POST)
- `/drinks-detail` (GET)
- `/drinks/<id>` (PATCH)
- `/drinks/<id>` (DELETE)
- `/menus` (POST)


##  Models

### drink
- id
- title
- recipe

### Menu
- id
- name


## Test app locally

run `python -m unittest discover -p test_app.py`
