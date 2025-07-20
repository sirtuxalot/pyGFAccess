from access import app
import json

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
    "password": "$2b$12$ZYuzjqJzR3dj2gzOYkPCwuzKtJLP1oQCPJJTgVCyPfbl2sfYgkBoO",
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

def test_register_failure_dup_email():
  """This will registration attempt will fail since there is an existing email in the users table"""
  data =  {
    "first_name": "Ruby",
    "last_name": "Yeomans",
    "email": "ry0517@proton.me",
    "address": "up the street",
    "city": "Delton",
    "state": "Michigan",
    "zip_code": "49046",
    "password": "$2b$12$8vdXMfFuTCBS0vcW9HSwn.0FTGGmHDre.Y0vAcwcB0WC29rpNgrFC",
    "subscription_id": 3,
    "access_level": 99,
  }
  response = app.test_client().post(
    '/register',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 409
  assert b'{"message":"UNAUTHORIZED: Provided Email already exists!"}\n' in response.data
