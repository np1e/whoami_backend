from flask import Blueprint, request, session, jsonify
from src.models import Game

bp = Blueprint("common", __name__)

@bp.route('/')
def index():
    return jsonify('Working')

@bp.route('/ping')
def ping():
    return jsonify('pong')


