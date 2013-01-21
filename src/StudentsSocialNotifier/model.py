import calendar
import os
from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from hashlib import sha256

from sqlalchemy import Column, Integer, UnicodeText, Date, DateTime, String, \
    BigInteger, Enum, SmallInteger, func, text, \
    Boolean

from sqlalchemy.orm import deferred
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()
metadata = Base.metadata


__all__ = ["User"]


# NOTE: This class is PostgreSQL specific. You should customize age() and the
# character column sizes if you want to use other databases.
class User(Base):
    """
    This example class represents a Facebook user. You can customize this class
    however you want.
    """

    __tablename__ = "users"


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    id = Column(Integer, autoincrement=True, primary_key=True)
    vk_id = Column(BigInteger, unique=True, index=True)
    name = Column(UnicodeText, nullable=True)
    surname = Column(UnicodeText, nullable=True)
    bydad = Column(UnicodeText, nullable=True)
    is_admin = Column(Boolean, default=False)
