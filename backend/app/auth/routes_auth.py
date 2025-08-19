from flask import Blueprint, jsonify, request
from app.models import User
from app import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    dados = request.get_json()
    email = dados.get('email', None)
    password = dados.get('password', None)

    if not email or not password:
        return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"erro": "Este e-mail já está em uso"}), 409

    new_user = User(email=email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"mensagem": f"Usuário {new_user.email} criado com sucesso!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login_user():

    dados = request.get_json()
    email = dados.get('email', None)
    password = dados.get('password', None)

    if not email or not password:
        return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"erro": "Credenciais inválidas"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)