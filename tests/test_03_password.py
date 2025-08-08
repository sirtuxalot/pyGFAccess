# tests/test_03_password.py

# local imports
from access import app
# external imports
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import json

# support functions

""" Read public key to encrypt the outgoing string """
def load_public_key():
  with open('keys/public_key.pem', 'rb') as pem_file:
    public_key = serialization.load_pem_public_key(pem_file.read())
  return public_key

""" Encrypt the ougoing password """
def encrypt_password(message, public_key):
  encrypted = public_key.encrypt(message.encode('utf-8'), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
  return base64.b64encode(encrypted).decode('utf-8')

# change password

def test_password():
  """ Change password of test user """
  password =  {
    "user_id": 2,
    "password": encrypt_password('ChangePass', load_public_key()),
  }
  response = app.test_client().post(
    '/password',
    data=json.dumps(password),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 200
  """ Ensure the provided email acquires the appropriate first and last name with changed password"""
  changed_pw =  {
    "email": "test.user@ist412.io",
    "password": encrypt_password('ChangePass', load_public_key())
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(changed_pw),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 200
  assert json.loads(response.data)["email"] == changed_pw["email"]
  assert json.loads(response.data)["first_name"] == "Test"
  assert json.loads(response.data)["last_name"] == "User"

def test_restored_pw():
  """ Restore original password """
  restore_pw =  {
    "user_id": 2,
    "password": encrypt_password('TestPass', load_public_key()),
  }
  response = app.test_client().post(
    '/password',
    data=json.dumps(restore_pw),
    headers={"Content-Type": "application/json"}
  )
  """ Ensure the provided email acquires the appropriate first and last name with restored password """
  restored_pw =  {
    "email": "test.user@ist412.io",
    "password": encrypt_password('TestPass', load_public_key())
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(restored_pw),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 200
  assert json.loads(response.data)["email"] == restored_pw["email"]
  assert json.loads(response.data)["first_name"] == "Test"
  assert json.loads(response.data)["last_name"] == "User"