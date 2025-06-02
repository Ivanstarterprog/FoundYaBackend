from flask import Flask
from .config import Config
from .extensions import db, migrate
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()

    from .routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app