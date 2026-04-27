import logging
import os
from flask import Flask, app
import urllib
from src.routes.auth import auth_bp
from src.routes.task import task_bp
from src.database.models import db

def create_app():
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s'
        )

    app = Flask(
        __name__,
        template_folder='../templates',
        static_folder='../static'
    )
    app.secret_key = 'replace-with-a-secure-secret'
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_DRIVER = os.getenv("DB_DRIVER")   

    params = urllib.parse.quote_plus(
    f"DRIVER={DB_DRIVER};"
    f"SERVER={DB_HOST};"
    f"DATABASE={DB_NAME};"
    "Trusted_Connection=yes;"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app