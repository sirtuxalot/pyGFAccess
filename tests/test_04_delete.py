# tests/test_04_delete.py

# local imports
from access import app
# external imports
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from flask import request
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
# delete user

def test_delete_user():
  """ Log in with user to delete """
  data =  {
    "email": "sy0623@mail.io",
    "password": encrypt_password('SadiePass', load_public_key())
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  """ verify user logged in and validate email """
  assert response.status_code == 200
  assert json.loads(response.data)["email"] == data["email"]
  user_id = json.loads(response.data)["user_id"]
  """ Change password of test user """
  delete_user =  {
    "user_id": user_id,
  }
  response = app.test_client().post(
    '/delete',
    data=json.dumps(delete_user),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 200