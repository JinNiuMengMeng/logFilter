from app.main import main as main_blueprint
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    app.config['SECRET_KEY'] = '123456'
    return app
