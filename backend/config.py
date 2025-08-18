# Este arquivo centraliza as configurações da nossa aplicação.
# A configuração mais importante aqui é a 'SQLALCHEMY_DATABASE_URI', que
# diz ao SQLAlchemy onde nosso banco de dados está localizado.
# 'os.path.abspath(os.path.dirname(__file__))' pega o caminho absoluto
# do diretório do projeto, garantindo que ele funcione em qualquer computador.
# 'sqlite:///...' indica que estamos usando um banco de dados SQLite
# localizado no arquivo 'fluxonota.db'.

import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False