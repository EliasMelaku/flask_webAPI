from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename_ = "Users"
    Username = db.Column(db.String, primary_key=True)
    Password = db.Column(db.String, nullable=False)
    FirstName = db.Column(db.String, primary_key=True)
    LastName = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False,unique=True)
    Address = db.Column(db.String, nullable=False)
    PhoneNumber = db.Column(db.String, nullable=False)
    Rating = db.Column(db.Integer, nullable=True)
    