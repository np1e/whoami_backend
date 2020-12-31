from flask import Blueprint, request, session, jsonify

bp = Blueprint("index", __name__)

@bp.route('/')
def index():
    return jsonify('Working')