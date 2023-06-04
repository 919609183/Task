from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class CarSchema(Schema):
    make = fields.String(required=True)
    model = fields.String(required=True)
    year = fields.String(required=True)
    category = fields.String(required=True)

   
