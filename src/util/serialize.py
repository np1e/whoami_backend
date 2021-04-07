from sqlalchemy.inspection import inspect
from src.db import db
from datetime import datetime, date
from enum import Enum

class Serializer(object):
    def serialize(self, exclude = []):
        d = {}
        for c in inspect(self).attrs.keys():
            if c in exclude:
                continue

            obj = getattr(self, c)

            if isinstance(obj, (datetime, date)):
                d[c] = obj.isoformat()
                continue

            if isinstance(obj, db.Model):
                d[c] = obj.serialize()
                continue
                
            if isinstance(obj, list):
                continue

            if isinstance(obj, Enum):
                print(obj)
                d[c] = obj.name
                continue
            
            d[c] = obj

        return d

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]