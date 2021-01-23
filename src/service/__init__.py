from src.db import get_db

def save_data(data):
    db = get_db()
    db.add(data)
    db.commit()