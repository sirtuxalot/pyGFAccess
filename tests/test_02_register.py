# tests/test_02_register.py

# local imports
from access import app
# external imports
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json

# support functions

"""Read public key to encrypt the outgoing string"""
def load_public_key():
  with open('keys/public_key.pem', 'rb') as pem_file:
    public_key = serialization.load_pem_public_key(pem_file.read())
  return public_key

"""Encrypt the ougoing password"""
def encrypt_password(message, public_key):
  encrypted = public_key.encrypt(message.encode('utf-8'), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
  return base64.b64encode(encrypted).decode('utf-8')

# Register

def test_register_success():
  """This will register a new user to the application"""
  data =  {
    "first_name": "Sadie",
    "last_name": "Yeomans",
    "email": "sy0623@mail.io",
    "address": "next county over",
    "city": "Lawton",
    "state": "Oklahoma",
    "zip_code": "73452",
    "password": encrypt_password('SadiePass', load_public_key()),
    "subscription_id": 4,
    "access_level": 99
  }
  response = app.test_client().post(
    '/register',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 201
  assert b'{"access_level":99,"address":"next county over","city":"Lawton","email":"sy0623@mail.io","first_name":"Sadie","last_name":"Yeomans","message":"SUCCESS: User successfully registered!","state":"Oklahoma","subscription_id":4,"zip_code":"73452"}\n' in response.data
  """Ensure the provided email acquires the appropriate first and last name"""
  data =  {
    "email": "sy0623@mail.io",
    "password": encrypt_password('SadiePass', load_public_key())
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 200
  assert json.loads(response.data)["email"] == data["email"]
  assert json.loads(response.data)["first_name"] == "Sadie"
  assert json.loads(response.data)["last_name"] == "Yeomans"

def test_register_failure_dup_email():
  """This will registration attempt will fail since there is an existing email in the users table"""
  data =  {
    "first_name": "Sadie",
    "last_name": "Yeomans",
    "email": "sy0623@mail.io",
    "address": "next county over",
    "city": "Lawton",
    "state": "Oklahoma",
    "zip_code": "73452",
    "password": encrypt_password('SadiePass', load_public_key()),
    "subscription_id": 4,
    "access_level": 99
  }
  response = app.test_client().post(
    '/register',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 409
  assert b'{"message":"UNAUTHORIZED: Provided Email already exists!"}\n' in response.data
