# access.py

# local imports
import seed_data
from models import db
# external imports
from dotenv import load_dotenv
from flask import Flask, jsonify, session
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

### Database settings
db.init_app(app)

# root level routes
@app.route('/', methods=['GET', 'POST'])
def login():
  return "login"

@app.route('/logout')
def logout():
  session.clear()  # Wipe out user and its token cache from session
  return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
  return "register"

if __name__ == '__main__':
  if venv_var is not None:
    app.run(debug=True, port=5001) 
  else:
    app.run(port=5001)
