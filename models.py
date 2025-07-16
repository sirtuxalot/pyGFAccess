# models/models.py

# external imports
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

# Subscriptions model
class subscriptions(db.Model):
  __tablename__ = 'subscriptions'
  subscription_id = db.Column(db.Integer, primary_key=True)
  subscription_name = db.Column(db.Text)
  rentals_allowed = db.Column(db.Integer)
  price = db.Column(db.Text)

  def __init__(self, subscription_name, rentals_allowed, price):
    self.subscription_name = subscription_name
    self.rentals_allowed = rentals_allowed
    self.price = price

# Users model
class users(db.Model):
  __tablename__ = 'users'
  user_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.Text)
  last_name = db.Column(db.Text)
  email = db.Column(db.Text, unique=True)
  address = db.Column(db.Text)
  city = db.Column(db.Text)
  state = db.Column(db.Text)
  zip_code = db.Column(db.Integer)
  password = db.Column(db.Text)
  subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.subscription_id'))
  access_level = db.Column(db.Integer)

  def __init__(self, first_name, last_name, email, address, city, state, zip_code, password, subscription_id, access_level):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.address = address
    self.city = city
    self.state = state
    self.zip_code = zip_code
    self.password = password
    self.subscription_id = subscription_id
    self.access_level = access_level
