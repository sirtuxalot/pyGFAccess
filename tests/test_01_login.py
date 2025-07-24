# tests/test_01_login.py

# local imports
from access import app
# external imports
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json

# application settings

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

# Login

def test_login_success():
  """Ensure the provided email acquires the appropriate first and last name"""
  data =  {
    "email": "test.user@ist412.io",
    "password": encrypt_password('TestPass', load_public_key())
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 200
  assert json.loads(response.data)["email"] == data["email"]
  assert json.loads(response.data)["first_name"] == "Test"
  assert json.loads(response.data)["last_name"] == "User"

def test_login_failure_email():
  """This login attempt should fail due to unknown email account, but throw back an ambiguous error"""
  data =  {
    "email": "test.user@ist412.iot",
    "password": encrypt_password('TestPass', load_public_key())
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 400
  assert b'{"message":"UNAUTHORIZED: 001 - Invalid credentials provided!"}\n' in response.data

def test_login_failure_password():
  """This login attempt should fail due to a bad password, but also throw back an ambiguous error"""
  data =  {
    "email": "test.user@ist412.io",
    "password": encrypt_password('wrong_password', load_public_key())
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 400
  assert b'{"message":"UNAUTHORIZED: 002 - Invalid credentials provided!"}\n' in response.data
