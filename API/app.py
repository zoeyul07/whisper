from flask import Flask
from flask_cors import CORS

from controllers.diary import diary_app

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(diary_app, url_prefix='/diary')
    return app
