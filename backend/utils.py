from flask_mail import Message, Mail
import json
from os import getenv


def read_api_config():
    try:
        with open('api.json', 'r') as json_file:
            data = json.load(json_file)[0]
            return data['API_SPECIFICATION']
    except FileNotFoundError as error:
        with open('backend/api.json', 'r') as json_file:
            data = json.load(json_file)[0]
            return data['API_SPECIFICATION']


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
