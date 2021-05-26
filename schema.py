from flask_marshmallow import Marshmallow
from dbModels import *

schema = Marshmallow()

class UserSchema(schema.Schema):
    class Meta:
        fields = ("Username", "Password", "FirstNmae", "LastName",
                  "Email", "Address", "PhoneNumber", "Rating")

        model = User