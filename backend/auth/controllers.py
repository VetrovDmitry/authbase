from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from datetime import datetime, timedelta, timezone
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from os import getenv
import json

from . import models
from backend.utils import UserError, AdminError, DeviceError, TokenError


class UserController:
    __model = models.User
    __salt = getenv('SERIALIZER_SALT', '')
    __serializer = URLSafeTimedSerializer(getenv('SECRET_KEY', ''))

    #  Checks

    @classmethod
    def check_username_exists(cls, username: str) -> dict:
        if cls.__model.find_by_username(username):
            return {'status': True, 'output': f"username: {username} exists"}
        return {'status': False, 'output': f"username: {username} does not exist"}

    @classmethod
    def check_email_exists(cls, email: str) -> dict:
        if cls.__model.find_by_email(email):
            return {'status': True, 'output': f"email: {email} exists"}
        return {'status': False, 'output': f"email: {email} does not exist"}

    #  Creates

    def signup_user(self, user_data: dict) -> dict:
        new_user = self.__model(
            first_name=user_data['firstName'],
            last_name=user_data['lastName'],
            username=user_data['username'],
            sex=user_data['sex'],
            birth_date=user_data['birth_date'],
            email=user_data['email'],
            password=user_data['password']
        )
        return new_user.public_info

    def generate_confirm_token(self, email: str) -> str:
        return self.__serializer.dumps(email, salt=self.__salt)

    def check_token(self, token: str) -> str:
        try:
            return self.__serializer.loads(token, salt=self.__salt, max_age=3600)
        except Exception:
            return ''




