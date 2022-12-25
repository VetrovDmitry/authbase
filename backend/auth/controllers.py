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


