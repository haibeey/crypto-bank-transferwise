import config, sqlite3, os,logging
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config_filename):

    app = Flask(__name__)
    app.config.from_object(config_filename)

    from app import api_bp, api
    app.register_blueprint(api_bp)

    jwt = JWTManager()
    jwt.init_app(app)

    jwt._set_error_handler_callbacks(app)


    CORS(app, support_credentials=True)

    logging.basicConfig(filename="error.log")

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)
