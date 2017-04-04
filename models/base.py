from flask_sqlalchemy import SQLAlchemy
from utils.config import read_config

db = SQLAlchemy()


def config_from_file(app):
    # read config
    config = read_config()

    # Create dummy secrey key so we can use sessions
    app.config['SECRET_KEY'] = config.get('app', 'secret_key')

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        config.get('db', 'sqlalchemy_database_uri')
    app.config['SQLALCHEMY_ECHO'] = \
        True if config.get('db', 'sqlalchemy_echo') == 'True' else False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
        True if \
        config.get('db', 'sqlalchemy_track_modifications') == 'True' \
        else False

    return app
