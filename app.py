import os
from models import setup_db
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)
  @app.route('/')
  def index():
    return 'Hello'
  
  @app.route('/hi')
  def hi():
    return 'hi'
  return app
app = create_app()