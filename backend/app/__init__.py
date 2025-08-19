from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config): 
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)

    
    db.init_app(app)
    migrate.init_app(app, db)

    from backend.app.auth.routes_auth import auth_bp
    from backend.app.documents.routes_doc import documents_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(documents_bp)

    from app import models

    return app