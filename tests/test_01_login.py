from access import app
import json

# Login

#def test_login_success(login_fix):
def test_login_success():
  """Ensure the provided email acquires the appropriate first and last name"""
  data =  {
    "email": "my0106@proton.me",
    "password": "$2b$12$ZYuzjqJzR3dj2gzOYkPCwuzKtJLP1oQCPJJTgVCyPfbl2sfYgkBoO"
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 200
  assert json.loads(response.data)["email"] == data["email"]
  assert json.loads(response.data)["first_name"] == "Max"
  assert json.loads(response.data)["last_name"] == "Yeomans"

#def test_login_failure_email(login_fix):
def test_login_failure_email():
  """Make sure we get an expected response from ccs log list index route"""
  data =  {
    "email": "my0106@protoon.me",
    "password": "$2b$12$ZYuzjqJzR3dj2gzOYkPCwuzKtJLP1oQCPJJTgVCyPfbl2sfYgkBoO"
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  assert response.status_code == 400
  assert b'{"message":"UNAUTHORIZED: Invalid credentials provided!"}\n' in response.data

#def test_login_failure_password(login_fix):
def test_login_failure_password():
  """Make sure we get an expected response from ccs log list index route"""
  data =  {
    "email": "my0106@proton.me",
    "password": "b@dP@5$w0rd"
  }
  response = app.test_client().post(
    '/login',
    data=json.dumps(data),
    headers={"Content-Type": "application/json"}
  )
  #assert response.status_code == 400
  assert b'{"message":"UNAUTHORIZED: Invalid credentials provided!"}\n' in response.data
