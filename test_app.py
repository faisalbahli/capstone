import json
import os

from flask_sqlalchemy import SQLAlchemy
from models import setup_db
import unittest
from app import app
from dotenv import load_dotenv

load_dotenv()

# set our application to testing mode.
app.testing = True
# Use this token or use your own token from /authorization/url endpoint.
JWT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdMSUQ2Y1dlQ1NNcTFFWEhwLVFzRyJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZS1zaG9wLXVkYWNpdHktcHJvamVjdC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBhZDYyZTY3YzgxZDMwMDcwY2ZmYWE5IiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjMyNDg3OTQyLCJleHAiOjE2MzI1NzI1NDIsImF6cCI6ImpPQmhSMnQwUDc5OXlBb09LOHV5TDJrdzNyTk1nZTRHIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyIsInBvc3Q6bWVudSJdfQ.E65dmVBYm99KUl5VS36xAYm0SUaoO-8v6FoN0cMvU99Ebb0ztK50eRBcO_V5n6EOCpXXyw-tWYoIgax_29gQADiWATgGiIS8y0WEpmzj7c9BeTxRnnMp83C8Vagxurluy5GlVsr8AVGN6n5gZz92EPc0KyNpy5w525aGkXNId74-NgDmPGfiu2fzUt40HwWKfazripGbih34SLF37YCzMHF5xRa-Pd6NXIUDOUJOcy3-_Ygshx4uu2cYGpDPDPu0z7NOt_MZrRRFDf7ur692RF4tNKZSrMHbJwSIlBtFLY1uUqGmnDG_8SFWCLQPDMl4nSRpdeoa-FVGTvSdPHpCTA"



class TestApi(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "coffee_shop"
        self.database_path = os.getenv('DATABASE_URL')# "postgresql://postgres:4279@localhost:5432/trivia"
        self.correct_drink = {
            "title":"7asasas77a as2",
            "recipe":[ { "color": "blue", "parts": 1 } ]
            }
        self.wrong_drink = {
            "title":"new-drink-4",
            }
        self.correct_menu = {
            "name":"new-menu"
            }
        self.wrong_menu = {
            "not-name":"new-menu"
            }
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

# get /drinks success
    def test_get_drinks_200(self):
        """Test _____________ """
        res = self.client().get('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])

# get /drinks fail
    def test_get_drinks_with_wrong_results(self):
        """Test _____________ """
        res = self.client().patch('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

# get /drinks-detail success
    def test_get_drinks_detail_200(self):
        """Test _____________ """
        res = self.client().get('/drinks-detail',  headers={'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])

# get /drinks-detail fail
    def test_get_drinks_detail_fail_405(self):
        """Test _____________ """
        res = self.client().post('/drinks-detail',  headers={'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

# post /drinks success
    def test_post_drinks_200(self):
        """Test _____________ """
        res = self.client().post(
            '/drinks',
            headers={'Authorization': 'Bearer ' + JWT_TOKEN},
            json=self.correct_drink)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])

# post /drinks fail
    def test_post_drinks_422(self):
        """Test _____________ """
        res = self.client().post(
            '/drinks',
            headers={'Authorization': 'Bearer ' + JWT_TOKEN},
            json=self.wrong_drink)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])


# patch /drinks/<id> success
    def test_patch_drinks_200(self):
        """Test _____________ """
        res = self.client().patch(
            '/drinks/93',
            headers={'Authorization': 'Bearer ' + JWT_TOKEN},
            json=self.correct_drink)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'
        ], True)
        self.assertTrue(data['drinks'])

# patch /drinks/<id> fail
    def test_patch_drinks_422(self):
        """Test _____________ """
        res = self.client().patch(
            '/drinks/100000000',
            headers={'Authorization': 'Bearer ' + JWT_TOKEN},
            json=self.correct_drink)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

# delete /drinks/<id> success
    def test_delete_drinks_200(self):
        """Test _____________ """
        res = self.client().delete(
            '/drinks/86',
            headers={'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], "86")
        self.assertEqual(data['success'], True)

# delete /drinks/<id> success
    def test_delete_drinks_422(self):
        """Test _____________ """
        res = self.client().delete(
            '/drinks/10000000',
            headers={'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])

# post /menus success
    def test_post_menu_200(self):
        """Test _____________ """
        res = self.client().post(
            '/menus',
            headers={'Authorization': 'Bearer ' + JWT_TOKEN},
            json=self.correct_menu)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['menus'])

# post /menus fail
    def test_post_menu_405(self):
        """Test _____________ """
        res = self.client().delete(
            '/menus',
            headers={'Authorization': 'Bearer ' + JWT_TOKEN},
            json=self.correct_menu)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'])