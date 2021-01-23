from src.model.models import Collection

def get_all_collections(): 
    return Collection.query.all()

def get_collection(name):
    return Collection.query.filter_by(name=name).first()