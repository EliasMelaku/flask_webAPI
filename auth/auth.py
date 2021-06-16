from flask import Flask, request
from flask.blueprints import Blueprint
from flask_marshmallow import Marshmallow
from flask_restplus import Api, Resource, fields
from werkzeug import cached_property

from schema import *

auth = Blueprint("auth", __name__, url_prefix="/auth")
# Set up schema to access the info from the database

api = Api(auth, version='1.0', title='DagmEbay API', 
          description="API for the dagm Ebay web serivce")

# first one to access 1, second one to access many
user_schema =  UserSchema()
users_schema = UserSchema(many=True)

ma = Marshmallow(auth)

# Model required by flask_restplus for expect

user = api.model("User", {
    'UserId':fields.String,
    'Username': fields.String,
    'Password':fields.String,
    'FirstName': fields.String, 
    'LastName': fields.String,
    'Email': fields.String,
    'Address': fields.String,
    'PhoneNumber': fields.String,
    'Rating': fields.Integer
})


@api.response(200, 'Return found users')
@api.route('/users/<string:username>')
class userResource(Resource):
    def get(self, username):
        # to display one user
        
        user = User.query.filter_by(Username=username).first()
        return user_schema.dump(user)
    

@api.route('/users')
class userResource(Resource):
    
    @api.expect(user)
    def post(self):
        # creates a new user
        
        new_user = User()
        new_user.UserId = request.json['UserId']
        new_user.Username = request.json['Username']
        new_user.Password = request.json['Password']
        new_user.FirstName = request.json['FirstName']
        new_user.LastName = request.json['LastName']
        new_user.Email = request.json['Email']
        new_user.Address = request.json['Address']
        new_user.PhoneNumber = request.json['PhoneNumber']
        new_user.Rating = 0
        
        check = User.query.filter_by(Username=new_user.Username).first()
        if check is not None:
            return 409
        
        db.session.add(new_user)
        db.session.commit()
        
        return user_schema.dump(new_user)
        