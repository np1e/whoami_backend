import jwt
import json
from flask import current_app 

ALGORITHM = "HS256"

def generate_token(identity):
    payload = {"_id": identity}
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm=ALGORITHM).decode('utf-8')

def get_claims(token):
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=ALGORITHM)
    except jwt.InvalidSignatureError:
        return None
