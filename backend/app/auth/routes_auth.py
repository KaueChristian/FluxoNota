from flask import Blueprint, jsonify, request
from app.models import User
from app import db
import uuid

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    new_token = str(uuid.uuid4())

    new_user = User(token=new_token)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully!',
        'user_id': new_user.id,
        'token': new_token
    }), 201
