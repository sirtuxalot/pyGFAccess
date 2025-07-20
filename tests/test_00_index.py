from access import app
import json

# Index

def test_index_get():
  """This should display the """
  response = app.test_client().get('/')
  assert response.status_code == 200
  assert b'[{"endpoint":"GET /","endpoint_description":"utilizes the index function that just provides simple documentation of the microservice endpoints","required_data":"None","returns":"a JSON object with this information as documentation"},{"endpoint":"POST /login","endpoint_description":"utilizes the login function which validates the user and provides user profile data back to pyGameFlix","required_data":"a JSON object with users email and encrypted password","returns":"a JSON object with users profile data"},{"endpoint":"GET /logout","endpoint_description":"utilizes the logout function which terminates the end user session within pyGameFlix","required_data":"TBD","returns":"TBD"},{"endpoint":"POST /register","endpoint_description":"utilizes the register function that receives the provided end user profile information and password and populates the users table within the pyGameFlix database","required_data":"a JSON object with the end users profile information and password","returns":"a JSON object with the end users profile information"}]\n' in response.data

def test_index_post():
  """Make sure that hitting the index sends to the login template"""
  response = app.test_client().post('/')
  assert response.status_code == 405
  assert b'<!doctype html>\n<html lang=en>\n<title>405 Method Not Allowed</title>\n<h1>Method Not Allowed</h1>\n<p>The method is not allowed for the requested URL.</p>\n' in response.data