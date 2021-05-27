from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from werkzeug import cached_property

import os

from dbModels import *
from schema import *


app = Flask(__name__)

# app configuration settings

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

# Set up the database
db.init_app(app)
ma = Marshmallow(app)

# Configure api

api = Api(app, version='1.0', title='DagmEbay API', 
          description="API for the dagm Ebay web serivce")

# Set up schema to access the info from the database

# first one to access 1, second one to access many
user_schema =  UserSchema()
users_schema = UserSchema(many=True)

# Model required by flask_restplus for expect

user = api.model("User", {
    'Username': fields.String,
    'FirstName': fields.String, 
    'LastName': fields.String,
    'Email': fields.String,
    'Address': fields.String,
    'PhoneNumber': fields.String,
    'Rating': fields.Integer
})


@api.route('/api/users/<string:username>')
class userResource(Resource):
    def get(self, username):
        # to display one user
        
        user = User.query.filter_by(Username=username).first()
        return user_schema.dump(user)
   