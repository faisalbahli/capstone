FSND Capstone Project

## URL

https://capstone-final-0.herokuapp.com/

There are two created accounts assigned with two roles in this project:

1- Manager (Authorized to all actions and endpoints)

Email : barista.role@gmail.com
Password: Capstone@1

Permissions for Manager:

Description:

- `delete:drinks` Remove drinks
- `get:drinks-detail` Get details about drink
- `patch:drinks` Modify drinks
- `post:drinks` Create new drink
- `post:menu` create new menu

2- Barista (Authorized to only GET /drinks-detail endpoint)

Email : barista.role@gmail.com
Password: Capstone@1 Permissions for Barista:

Description:

- `get:drinks-detail` Get details about drink

The following endpoints are in the app:

- `/drinks (GET)`
- `/drinks (POST)`
- `/drinks-detail` (GET)
- `/drinks/<id>` (PATCH)
- `/drinks/<id>` (DELETE)

There is extra endpoint to get authorized and get the access token from the URL to test it if needed in Postman, which is:

- `authorization/url` (GET)

### Test app locally

run `python -m unittest discover -p test_app.py`
