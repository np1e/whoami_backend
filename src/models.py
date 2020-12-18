from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from .db import Base

class Player(Base):
    __tablename__ = "Players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)

    def __init__(self, username=None):
            self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)