from flask import Blueprint, jsonify, request
from app.models import User, Document # Adicione a importação do User
from app import db
# Importe os decoradores e funções do Flask-JWT-Extended
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

documents_bp = Blueprint('documents', __name__, url_prefix='/api/documents')

# O decorador @jwt_required() agora protege a rota.
# Ele verificará o 'Authorization: Bearer <token>' header automaticamente.
@documents_bp.route('/<string:documento_id>', methods=['GET'])
@jwt_required()
def get_documento_por_id(documento_id):
    # A função get_jwt_identity() retorna o que definimos como 'identity' no login (o user.id)
    current_user_id = get_jwt_identity()
    
    doc = Document.query.get(documento_id)
    if not doc or doc.user_id != current_user_id:
        return jsonify({"erro": "Documento não encontrado ou sem permissão"}), 404
    
    # ... (o resto da função continua igual)
    return jsonify({
        "id": doc.id,
        "titulo": doc.titulo,
        "conteudo": doc.conteudo,
        "diagrama": json.loads(doc.diagrama_json or '{}')
    })

# Aplique as mesmas mudanças para as outras rotas (POST, PUT, DELETE)

@documents_bp.route('', methods=['POST'])
@jwt_required()
def create_documento():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id) # Buscamos o objeto User
    
    dados = request.get_json()
    if not dados or 'titulo' not in dados:
        return jsonify({"erro": "O título é obrigatório"}), 400
    
    novo_doc = Document(
        titulo=dados['titulo'],
        conteudo=dados.get('conteudo', ''),
        diagrama_json=json.dumps(dados.get('diagrama', {})),
        owner=current_user # Associamos o documento ao usuário
    )
    db.session.add(novo_doc)
    db.session.commit()
    
    return jsonify({"id": novo_doc.id, "titulo": novo_doc.titulo}), 201

# Lembre-se de atualizar também as rotas de PUT e DELETE
# para usar @jwt_required() e get_jwt_identity()
@documents_bp.route('/<string:documento_id>', methods=['PUT'])
@jwt_required()
def update_documento(documento_id):
    current_user_id = get_jwt_identity()
    doc = Document.query.get(documento_id)
    if not doc or doc.user_id != current_user_id:
        return jsonify({"erro": "Documento não encontrado ou sem permissão"}), 404

    dados = request.get_json()
    doc.titulo = dados.get('titulo', doc.titulo)
    doc.conteudo = dados.get('conteudo', doc.conteudo)
    if 'diagrama' in dados:
        doc.diagrama_json = json.dumps(dados['diagrama'])
    
    db.session.commit()
    return jsonify({"mensagem": "Documento atualizado com sucesso"})
    
@documents_bp.route('/<string:documento_id>', methods=['DELETE'])
@jwt_required()
def delete_documento(documento_id):
    current_user_id = get_jwt_identity()
    doc = Document.query.get(documento_id)
    if not doc or doc.user_id != current_user_id:
        return jsonify({"erro": "Documento não encontrado ou sem permissão"}), 404
    
    db.session.delete(doc)
    db.session.commit()
    return jsonify({"mensagem": "Documento deletado com sucesso"})