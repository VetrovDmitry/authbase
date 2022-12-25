from marshmallow import Schema, fields, post_load, validate
from .models import HumanGender, UserStatus, AdminStatus, DeviceStatus
from backend.utils import UnprocessableEntity


class NewUserSchema(Schema):
    firstName = fields.Str(validate=[validate.Length(1, 50), validate.Regexp(r"^[a-zA-Z]+$")], required=True)
    lastName = fields.Str(validate=[validate.Length(1, 50), validate.Regexp(r"^[a-zA-Z]+$")], required=True)
    username = fields.Str(validate=[validate.Length(1, 50), validate.Regexp(r"^[a-zA-Z0-9_]+$")], required=True)
    sex = fields.Str(validate=[validate.OneOf(HumanGender.values())], required=True)
    birthDate = fields.Date(required=True)
    email = fields.Email(validate=[validate.Length(1, 100)], required=True)
    password = fields.Str(validate=[validate.Length(7, 50), validate.Regexp(r"^[a-zA-Z0-9]+$")], required=True)

    @post_load
    def prepare_data(self, in_data, **kwargs):
        in_data['firstName'] = in_data.get('firstName').lower().capitalize()
        in_data['lastName'] = in_data.get('lastName').lower().capitalize()
        in_data['username'] = in_data.get('username').lower()
        in_data['sex'] = in_data.get('sex')
        in_data['birthDate'] = in_data.get('birthDate')
        in_data['email'] = in_data.get('email').lower()
        in_data['password'] = in_data.get('password')
