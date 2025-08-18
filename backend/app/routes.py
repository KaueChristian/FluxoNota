# Usamos um dicionário chamado 'documentos' para simular um banco de dados em memória.
# Cada função (ex: get_documentos, create_documento) corresponde a uma operação CRUD.
# - @app.route(...): É um "decorador" do Flask que transforma uma função Python comum em uma rota de API.
# - methods=[...]: Especifica quais métodos HTTP a rota aceita (GET, POST, etc.).
# - jsonify: Uma função do Flask que converte dicionários Python para o formato JSON, que é a linguagem universal das APIs.
# - request: Um objeto do Flask que contém as informações da requisição que o frontend enviou, incluindo os dados JSON.

from flask import Flask, jsonify, request
from app.models import User, Document
from app import db
import json

def init_app(app):

    def validate_token():
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return None
        token = token.split(' ')[1]
        user = User.query.filter_by(token=token).first()
        return user
    
    @app.route('/api/documentos/<documento_id>', methods=['GET'])
    def get_documento_por_id(documento_id):
        user = validate_token()
        if not user:
            return jsonify({"erro": "Acesso não autorizado"}), 401

        doc = Document.query.get(documento_id)
        if not doc or doc.user_id != user.id:
            return jsonify({"erro": "Documento não encontrado ou sem permissão"}), 404
        
        return jsonify({
            "id": doc.id,
            "titulo": doc.titulo,
            "conteudo": doc.conteudo,
            "diagrama": json.loads(doc.diagrama_json or '{}')
        })
    
    @app.route('/api/documentos', methods=['POST'])
    def create_documento():
        user = validate_token()
        if not user:
            return jsonify({"erro": "Acesso não autorizado"}), 401

        dados = request.get_json()
        if not dados or 'titulo' not in dados:
            return jsonify({"erro": "O título é obrigatório"}), 400
        
        novo_doc = Document(
            titulo=dados['titulo'],
            conteudo=dados.get('conteudo', ''),
            diagrama_json=json.dumps(dados.get('diagrama', {})),
            owner=user
        )
        db.session.add(novo_doc)
        db.session.commit()
        
        return jsonify({"id": novo_doc.id, "titulo": novo_doc.titulo}), 201
    
    @app.route('/api/documentos/<documento_id>', methods=['PUT'])
    def update_documento(documento_id):
        user = validate_token()
        if not user:
            return jsonify({"erro": "Acesso não autorizado"}), 401
        
        doc = Document.query.get(documento_id)
        if not doc or doc.user_id != user.id:
            return jsonify({"erro": "Documento não encontrado ou sem permissão"}), 404

        dados = request.get_json()
        doc.titulo = dados.get('titulo', doc.titulo)
        doc.conteudo = dados.get('conteudo', doc.conteudo)
        if 'diagrama' in dados:
            doc.diagrama_json = json.dumps(dados['diagrama'])
        
        db.session.commit()
        return jsonify({"mensagem": "Documento atualizado com sucesso"})
        
    @app.route('/api/documentos/<documento_id>', methods=['DELETE'])
    def delete_documento(documento_id):
        user = validate_token()
        if not user:
            return jsonify({"erro": "Acesso não autorizado"}), 401
        
        doc = Document.query.get(documento_id)
        if not doc or doc.user_id != user.id:
            return jsonify({"erro": "Documento não encontrado ou sem permissão"}), 404
        
        db.session.delete(doc)
        db.session.commit()
        return jsonify({"mensagem": "Documento deletado com sucesso"})