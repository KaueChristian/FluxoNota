# Este arquivo define as "plantas" das nossas tabelas do banco de dados.
# Cada classe é uma tabela.
# - User: Armazena nossos usuários. Por enquanto, só terá id e token.
# - Document: Armazena os documentos.
#   - O campo 'user_id' é uma "chave estrangeira" (ForeignKey) que aponta para o id na tabela User.
#   - 'db.relationship' cria a mágica da relação:
#     - Em User, 'documents' nos dará uma lista de todos os documentos daquele usuário.
#     - Em Document, 'owner' nos dará o objeto User dono daquele documento.
#   - O campo 'id' de Document agora é uma String para armazenar o UUID.

import uuid
from app import db

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    token = db.Column(db.String(128), unique=True, nullable=False)
    documents = db.relationship('Document', backref='owner', lazy=True)

class Document(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.Text, nullable=True)
    diagrama_json = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)