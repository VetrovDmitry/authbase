from flask_mail import Message, Mail
from flask import current_app
import json
from os import getenv
from werkzeug.exceptions import UnprocessableEntity
from functools import wraps
from dataclasses import dataclass


device_header = {'apiKeyAuth': []}
user_header = {'JWT': []}

api_key_scheme = {
    'type': 'apiKey',
    'in': 'header',
    'name': 'X-API-Key',
    'required': True
}
jwt_scheme = {
    'type': 'apiKey',
    'in': 'header',
    'name': 'X-AUTH-Key',
    'required': True
}


def read_api_config():
    try:
        with open('api.json', 'r') as json_file:
            data = json.load(json_file)[0]
            return data['API_SPECIFICATION']
    except FileNotFoundError as error:
        with open('backend/api.json', 'r') as json_file:
            data = json.load(json_file)[0]
            return data['API_SPECIFICATION']


#  Errors


@dataclass
class UserError(Exception):
    message: str = 'some problem with user'
    code: int = 400


@dataclass
class AdminError(Exception):
    message: str = 'some problem with admin'
    code: int = 400


@dataclass
class DeviceError(Exception):
    message: str = 'some problem with device'
    code: int = 400


@dataclass
class TokenError(Exception):
    message: str = 'some problem with token'
    code: int = 400


def error_handler(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (UserError, AdminError, DeviceError, TokenError) as err:
            current_app.logger.error(err.message)
            return {'message': err.message}, err.code
        except UnprocessableEntity as error:
            message = error.description
            current_app.logger.error(message)
            return {'message': message}, 422
        except Exception as error:
            current_app.logger.error(error)
            return {'message': error}, 500

    return decorator


def ep_responses(responses: list) -> dict:
    prepared_responses = dict()
    for code, description in responses:
        prepared_responses[f"{code}"] = {
            "content": {"application/json": {"schema": "Gist"}},
            "description": description
        }
    return prepared_responses


mail = Mail()


class MailController:
    @property
    def frontend_url(self) -> str:
        return getenv('REACT_APP_URL', '')

    @staticmethod
    def html_template(text: str) -> str:
        return f"""
            {text}
        """

    def send_confirmation(self, email: str, fullname: str, confirm_token: str) -> None:
        with mail.connect() as conn:
            message = Message('E-mail confirmation', recipients=[email])
            message.html = self.html_template(f"""Welcome to the space, {fullname}! Go to this page
                <a href="{self.frontend_url}/confirm-registration/{confirm_token}">page</a>
                for confirmation completing. Hope you enjoy it...""")
            conn.send(message)
