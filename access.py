# access.py

# local imports
from models import db, users
# external imports
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session
import logging
import os

# read environment file
load_dotenv()

# application settings
app = Flask(__name__)

# checking for virtual environment
venv_var = os.getenv('VIRTUAL_ENV', default=None)
if venv_var is not None:
  logging.basicConfig(level=logging.DEBUG)
  logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
  logging.info('***** Debug Logging: on *****')
else:
  logging.basicConfig=logging.INFO

# database connection setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Database settings
db.init_app(app)

# root level routes
@app.route('/')
def index():
  msg = [
    {
      'endpoint': 'index (/)',
      'endpoint_description': 'provides simple documentation for endpoints',
      'required_entries': 'None',
      'returned_data': 'None',
    },
    {
      'endpoint': 'login (/login)',
      'endpoint_description': 'validates end user login and provides session data back to pyGameFlix',
      'required_entries': 'None',
      'returned_data': 'None',
    },
    {
      'endpoint': 'logout (/logout)',
      'endpoint_description': 'terminates end user session within pyGameFlix',
      'required_entries': 'None',
      'returned_data': 'None',
    },
    {
      'endpoint': 'register (/register)',
      'endpoint_description': 'registers new pyGameFlix end user',
      'required_entries': 'None',
      'returned_data': 'None',
    },
  ]
  return jsonify(msg)
  
@app.route('/login', methods=['POST'])
def login():
  email = request.json['email']
  password = request.json['password']
  userProfile = users.query.filter_by(email=email).first()
  logging.debug(userProfile)
  if userProfile is None or password != userProfile.password:
    msg = {
      'UNAUTHORIZED': 'Invalid credentials provided!'
    }
  else:
    msg = {
      'first_name': userProfile.first_name,
      'last_name': userProfile.last_name,
      'email': userProfile.email,
      'address': userProfile.address,
      'city': userProfile.city,
      'state': userProfile.state,
      'zip_code': userProfile.zip_code,
      'subscription_id': userProfile.subscription_id,
      'access_level': userProfile.access_level,
    }
  return jsonify(msg)

@app.route('/logout')
def logout():
  msg = {"message":"/logout endpoint accessed"}
  return jsonify(msg)

@app.route('/register', methods=['POST'])
def register():
  first_name = request.json['first_name']
  last_name = request.json['last_name']
  email = request.json['email']
  address = request.json['address']
  city = request.json['city']
  state = request.json['state']
  zip_code = request.json['zip_code']
  password = request.json['password']
  subscription_id = request.json['subscription_id']
  access_level = request.json['access_level']
  newUser = users(first_name, last_name, email, address, city, state, zip_code, password, subscription_id, access_level)
  db.session.add(newUser)
  db.session.commit()
  msg = {
    'first_name': first_name,
    'last_name': last_name,
    'email': email,
    'address': address,
    'city': city,
    'state': state,
    'zip_code': zip_code,
    'subscription_id': subscription_id,
    'access_level': access_level,
  }
  return jsonify(msg)

if __name__ == '__main__':
  if venv_var is not None:
    app.run(debug=True, port=5001) 
  else:
    app.run(port=5001)
