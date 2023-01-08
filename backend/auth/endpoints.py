from flask import current_app, after_this_request, request
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from . import controllers
from . import schemas
from backend.utils import (UserError, TokenError, DeviceError, AdminError, MailController,
                           error_handler, ep_responses, device_header, user_header)


AUTH = 'Auth operations'


class AddUserApi(MethodResource):
    __controller = controllers.UserController()
    __mail_controller = MailController()
    __schemas = {
        'request': schemas.NewUserSchema,
        'response': schemas.PublicUserSchema
    }
    decorators = [
        error_handler
    ]

    @doc(tags=[AUTH],
         summary='uploads new user',
         description='receives new user info',
         security=[device_header],
         responses=ep_responses([(409, "username or email exists")]))
    @use_kwargs(__schemas['request'], location='form')
    @marshal_with(__schemas['response'], code=201)
    def post(self, **user_data):

        username_checking = self.__controller.check_username_exists(user_data['username'])
        if username_checking['status']:
            raise UserError(username_checking['output'], 409)

        email_checking = self.__controller.check_email_exists(user_data['email'])
        if email_checking['status']:
            raise UserError(email_checking['output'], 409)

        result = self.__controller.signup_user(user_data)
        confirm_token = self.__controller.generate_confirm_token(result['email'])
        self.__mail_controller.send_confirmation(result['email'], result['fullname'], confirm_token)
        response = self.__schemas['response']().load(result)

        current_app.logger.info(f"user: {result['id']} signed up")

        return response, 201

