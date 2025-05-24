from flask import Flask
from .config import Config
from .extensions import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    # регистрируем роуты
    from .routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
