from flask import Blueprint, jsonify, request
from app.models import Document
from app import db
from app.utils.decorators import token_required
import json

documents_bp = Blueprint('documents', __name__, url_prefix='/api/documents')

@documents_bp.route('/<string:document_id>', methods=['GET'])
@token_required
def get_document(current_user, document_id):
    doc = Document.query.get(document_id)
    if not doc or doc.user_id != current_user.id:
        return jsonify({'message': 'Document not found or access denied!'}), 404

    return jsonify({
        "id": doc.id,
        "titulo": doc.titulo,
        "conteudo": doc.conteudo,
        "diagrama": json.loads(doc.diagrama_json or '{}')
    })

@documents_bp.route('', methods=['POST'])
@token_required
def create_document(current_user):
    dados = request.get_json()
    if not dados or 'titulo' not in dados:
        return jsonify({'message': 'Invalid data! Title is required.'}), 400
    
    novo_doc = Document(
        titulo=dados['titulo'],
        conteudo=dados.get('conteudo', ''),
        diagrama_json=json.dumps(dados.get('diagrama', {})),
        owner=current_user
    )
    db.session.add(novo_doc)
    db.session.commit()
    
    return jsonify({"id": novo_doc.id, "titulo": novo_doc.titulo}), 201

@documents_bp.route('/<string:document_id>', methods=['PUT'])
@token_required
def update_document(current_user, document_id):
    doc = Document.query.get(document_id)
    if not doc or doc.user_id != current_user.id:
        return jsonify({'message': 'Document not found or access denied!'}), 404
    
    data = request.get_json()
    doc.titulo = data.get('titulo', doc.titulo)
    doc.conteudo = data.get('conteudo', doc.conteudo)
    if 'diagrama' in data:
        doc.diagrama_json = json.dumps(data['diagrama'])
    
    db.session.commit()
    return jsonify({"message": "Document updated successfully!"}), 200

@documents_bp.route('/<string:document_id>', methods=['DELETE'])
@token_required
def delete_document(current_user, document_id):
    doc = Document.query.get(document_id)
    if not doc or doc.user_id != current_user.id:
        return jsonify({'message': 'Document not found or access denied!'}), 404
    
    db.session.delete(doc)
    db.session.commit()
    
    return jsonify({"message": "Document deleted successfully!"}), 200