# access.py

# local imports
from models import db, users
# external imports
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
import jwt
from pathlib import Path
import logging
import os

# read environment file
load_dotenv()

# application settings
app = Flask(__name__)
bcrypt = Bcrypt()

# checking for virtual environment
venv_var = os.getenv('VIRTUAL_ENV', default=None)
if venv_var is not None:
  logging.basicConfig(level=logging.DEBUG)
  logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
  logging.info('***** Debug Logging: on *****')
else:
  logging.basicConfig = logging.INFO

# database connection setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Database settings
db.init_app(app)

# support functions

def create_jwt():
  now = datetime.now(timezone.utc)
  payload = {
    'iss': 'http://pygameflix.io',
    'sub': os.urandom(24).decode('ISO-8859-1'),
    'iat': now,
    'exp': (now + timedelta(hours=24)).timestamp(),
  }
  private_key_text = Path("keys/private_key.pem").read_text()
  private_key = serialization.load_pem_private_key(
    private_key_text.encode(), password=None
  )
  return jwt.encode(payload=payload, key=private_key, algorithm="RS256")

def load_private_key(password=None):
  with open('keys/private_key.pem', 'rb') as pem_file:
    private_key = serialization.load_pem_private_key(pem_file.read(), password=password.encode() if password else None)
    return private_key

def decrypt_password(encrypted_b64, private_key):
  encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
  decrypted = private_key.decrypt(encrypted, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
  return decrypted.decode('utf-8')

# root level routes

@app.route('/')
def index():
  msg = [
    {
      'endpoint': 'GET /',
      'endpoint_description': 'utilizes the index function that just provides simple documentation of the microservice endpoints',  # noqa: E501
      'required_data': 'None',
      'returns': 'a JSON object with this information as documentation',
    },
    {
      'endpoint': 'POST /login',
      'endpoint_description': 'utilizes the login function which validates the user and provides user profile data back to pyGameFlix',  # noqa: E501
      'required_data': 'a JSON object with users email and encrypted password',
      'returns': 'a JSON object with users profile data',
    },
    {
      'endpoint': 'GET /logout',
      'endpoint_description': 'utilizes the logout function which terminates the end user session within pyGameFlix',
      'required_data': 'TBD',
      'returns': 'TBD',
    },
    {
      'endpoint': 'POST /register',
      'endpoint_description': 'utilizes the register function that receives the provided end user profile information and password and populates the users table within the pyGameFlix database',  # noqa: E501
      'required_data': 'a JSON object with the end users profile information and password',
      'returns': 'a JSON object with the end users profile information',
    },
    {
      'endpoint': 'POST /password',
      'endpoint_description': 'utilizes the password function to change the password of the user',  # noqa: E501
      'required_data': 'a JSON object with the end users user_id and password',
      'returns': 'a JSON object with just a success or failure message',
    },
    {
      'endpoint': 'POST /delete',
      'endpoint_description': 'utilizes the delete function to completely delete the user',  # noqa: E501
      'required_data': 'a JSON object with just the end users user_id',
      'returns': 'a JSON object with just a success or failure message',
    },
  ]
  return jsonify(msg)

@app.route('/login', methods=['POST'])
def login():
  """ map email and encryped password from incoming json to function variables """
  email = request.json['email']
  password = decrypt_password(request.json['password'], load_private_key())
  """ retrieve user prfile from users table by unique email address """
  userProfile = users.query.filter_by(email=email).first()
  """ test for empty user profile and compare incoming password versus stored password """
  if userProfile is not None:
    if bcrypt.check_password_hash(userProfile.password, password):
      """ build json message to return to pyGameFlix """
      msg = {
        'message': 'SUCCESS: User credentials authenticated!',
        'user_id': userProfile.user_id,
        'first_name': userProfile.first_name,
        'last_name': userProfile.last_name,
        'email': userProfile.email,
        'address': userProfile.address,
        'city': userProfile.city,
        'state': userProfile.state,
        'zip_code': userProfile.zip_code,
        'subscription_id': userProfile.subscription_id,
        'access_level': userProfile.access_level,
        'jwt_token': create_jwt(),
      }
      return_code = 200
    else:  
      msg = {
        'message': 'UNAUTHORIZED: 002 - Invalid credentials provided!'
      }
      return_code = 400
  else:
    """ login failed """
    msg = {
      'message': 'UNAUTHORIZED: 001 - Invalid credentials provided!'
    }
    return_code = 400
  return jsonify(msg), return_code

@app.route('/logout')
def logout():
  msg = {"message": "/logout endpoint accessed"}
  return jsonify(msg)

@app.route('/register', methods=['POST'])
def register():
  """ map incoming json to function variables """
  first_name = request.json['first_name']
  last_name = request.json['last_name']
  email = request.json['email']
  address = request.json['address']
  city = request.json['city']
  state = request.json['state']
  zip_code = request.json['zip_code']
  password = decrypt_password(request.json['password'], load_private_key())
  subscription_id = request.json['subscription_id']
  access_level = request.json['access_level']
  """ re-enforce prevention of duplicate emails by checking before adding uses """
  emailVerification = users.query.filter_by(email=email).first()
  if emailVerification is None:
    """ decode password for database storage """
    bcrypt_password = bcrypt.generate_password_hash(password).decode('utf-8')
    """ create newUser variable with users table using function variables """
    newUser = users(first_name, last_name, email, address, city, state, zip_code, bcrypt_password, subscription_id, access_level)
    """ add and commit newUser variable to database """
    db.session.add(newUser)
    db.session.commit()
    """ build json message to return to pyGameFlix """
    msg = {
      'message': 'SUCCESS: User successfully registered!',
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
    return_code = 201
  else:
    msg = {
      'message': 'UNAUTHORIZED: Provided Email already exists!'
    }
    return_code = 409
  return jsonify(msg), return_code

@app.route('/password', methods=['POST'])
def password():
  """ map incoming json to function variables """
  user_id = request.json['user_id']
  password = decrypt_password(request.json['password'], load_private_key())
  """ decode password for database storage """
  bcrypt_password = bcrypt.generate_password_hash(password).decode('utf-8')
  """ retrieve user data """
  password_edit = users.query.get_or_404(user_id)
  """ the line above works as intended, but throws a warning, the following does not throw a working or work as needed
  password_edit = db.session.query(users.password).filter(users.user_id==user_id)
  """
  password_edit.password = bcrypt_password
  db.session.commit()
  msg = {
    'message': 'SUCCESS: Password updated.',
  }
  return jsonify(msg)

@app.route('/delete', methods=['POST'])
def delete():
  """ map incoming json to function variables """
  user_id = request.json['user_id']
  user_delete = users.query.get_or_404(user_id)
  db.session.delete(user_delete)
  db.session.commit()
  msg = {
    'message': 'SUCCESS: Password updated.',
  }
  return jsonify(msg)

if __name__ == '__main__':
  if venv_var is not None:
    app.run(debug=True, port=5001)
  else:
    app.run(port=5001)
