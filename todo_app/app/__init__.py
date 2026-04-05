from flask import Flask
from app.models import db
from app.routes.auth import auth_bp
from app.routes.task import task_bp

def create_app():
    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )
    app.secret_key = 'replace-with-a-secure-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app
