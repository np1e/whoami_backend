from sqlalchemy.inspection import inspect
from src.db import db

class Serializer(object):
    def serialize(self):
        d = {}
        for c in inspect(self).attrs.keys():
            obj = getattr(self, c)

            if isinstance(obj, (datetime, date)):
                d[c] = obj.isoformat()
                continue
                
            if isinstance(obj, db.Model):
                d[c] = obj.serialize()
            
            d[c] = obj

        return d
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]