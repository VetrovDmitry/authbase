from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_bcrypt import generate_password_hash, check_password_hash
from uuid import uuid4
import enum
import datetime

from backend.database import db, Base


class HumanGender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'

    @classmethod
    def values(cls) -> list:
        return [cls.MALE.value, cls.FEMALE.value]


class UserStatus(enum.Enum):
    UNCONFIRMED = 'unconfirmed'
    CONFIRMED = 'confirmed'
    FROZEN = 'frozen'
    DELETED = 'deleted'

    @classmethod
    def values(cls) -> list:
        return [cls.UNCONFIRMED.value, cls.CONFIRMED.value, cls.FROZEN.value, cls.DELETED.value]


class User(db.Model, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    sex = Column(Enum(HumanGender))
    birth_date = Column(Date, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hash = Column(String(255), nullable=False)
    status = Column(Enum(UserStatus))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    admin = relationship('Admin', back_populates='user', uselist=False, lazy=True)
    tokens = relationship('Token', back_populates='user', uselist=True)

    def __init__(self, first_name: str, last_name: str, username: str, sex: str, birth_date: datetime.date,
                 email: str, password: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.sex = HumanGender(sex)
        self.birth_date = birth_date
        self.email = email
        self.hash = self.create_hash(password)
        self.status = UserStatus('unconfirmed')
        self.upload()

    def __repr__(self):
        return f"user: {self.fullname}"

    @property
    def fullname(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def public_info(self) -> dict:
        return {
            'id': self.id,
            'fullName': self.fullname,
            'username': self.username,
            'email': self.email,
            'time_created': self.time_created.isoformat()
        }

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def create_hash(password: str) -> str:
        return generate_password_hash(password).decode('UTF-8')

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.hash, password)



class AdminStatus(enum.Enum):
    ADMIN = 'admin'
    MODER = 'moder'

    @classmethod
    def values(cls) -> list:
        return [cls.ADMIN.value, cls.MODER.value]


class Admin(db.Model, Base):
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    status = Column(Enum(AdminStatus))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User', back_populates='admin', uselist=False, lazy=True)
    devices = relationship('Device', back_populates='admin', uselist=True)


class DeviceStatus(enum.Enum):
    ENABLE = 'enable'
    DISABLE = 'disable'

    @classmethod
    def values(cls) -> list:
        return [cls.ENABLE.value, cls.DISABLE.value]


class Device(db.Model, Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey('admins.id'))
    name = Column(String(80), nullable=False, unique=True)
    key = Column(String(255))
    status = Column(Enum(DeviceStatus))
    requests = Column(Integer, default=0)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    admin = relationship('Admin', back_populates='devices', uselist=False)
    tokens = relationship('Token', back_populates='device', uselist=True)


class TokenStatus(enum.Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'

    @classmethod
    def values(cls) -> list:
        return [cls.ACTIVE.value, cls.EXPIRED.value]


class Token(db.Model, Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(Text, unique=True)
    refresh_token = Column(Text, unique=True)
    expires = Column(DateTime(timezone=True))
    status = Column(Enum(TokenStatus))

    user = relationship('User', back_populates='tokens', uselist=False)
    device = relationship('Device', back_populates='tokens', uselist=True)
