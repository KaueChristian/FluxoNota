from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class): 
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes
    routes.init_app(app)

    from app import models

    return app