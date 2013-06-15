import calendar
import os
from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from hashlib import sha256

from sqlalchemy import Column, Integer, UnicodeText, Date, DateTime, String, \
    BigInteger, Enum, SmallInteger, func, text, \
    Boolean, ForeignKey

from sqlalchemy.orm import deferred, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()
metadata = Base.metadata

from sqlalchemy.types import TypeDecorator, VARCHAR
import json

class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage:

        JSONEncodedDict(255)

    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        return json.loads(value) if value is not None else []


__all__ = ['User', 'Post', 'Delivery', 'PeriodicDeliveryTask']


class User(Base):
    """
    This example class represents a VK user.
    """

    __tablename__ = "users"


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    id = Column(Integer, autoincrement=True, primary_key=True)
    vk_id = Column(BigInteger, unique=True, index=True)
    name = Column(String(32), nullable=True)
    surname = Column(String(32), nullable=True)
    bydad = Column(String(32), nullable=True)
    is_admin = Column(Boolean, default=False)


class Post(Base):
    """
    This class represents a message to share.
    """

    __tablename__ = "posts"


    def __init__(self, **kwargs):
        super(Post, self).__init__(**kwargs)

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(32), nullable=True)
    content = Column(String(256), nullable=False)
    link = Column(String(256), nullable=True)
    created = Column(DateTime, default=datetime.utcnow, server_default=text("now()"), nullable=False)
    show = Column(Boolean, default=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship("User", backref="posts_written")


class Delivery(Base):
    """
    This class represents status of message delivery to user.
    """

    __tablename__ = "delivery"


    def __init__(self, **kwargs):
        super(Delivery, self).__init__(**kwargs)

    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    is_read = Column(Boolean, default=False)
    notified_via_vk = Column(Boolean, default=False)
    notified_via_email = Column(Boolean, default=False)

    user = relationship("User", backref="delivery_assocs")
    post = relationship("Post", backref="delivery_assocs")

class PeriodicDeliveryTask(Base):
    """
    This class represents a periodic task delivery schedule.
    """

    __tablename__ = "periodic_delivery_task"


    def __init__(self, **kwargs):
        super(PeriodicDeliveryTask, self).__init__(**kwargs)

    id = Column(Integer, autoincrement=True, primary_key=True)
    when = Column(DateTime)
    todo = Column(JSONEncodedDict(256))
    status = Column(Enum('SCHEDULED', 'FAILED', 'SUCCEDED'), default='SCHEDULED')
