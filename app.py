from flask import Flask
from extensions import migrate, db
import os

basedir = os.path.abspath(os.path.dirname(__file__))

config = {
    "DEBUG": True,          # some Flask specific configs
    "SQLALCHEMY_DATABASE_URI":"sqlite:///"+os.path.join(basedir, "db.sqlite3"),
    'SECRET_KEY':'super secret key'
}


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_mapping(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    return app

app = create_app(config)
from views import *

if __name__ == "__main__":
    app.run(debug=True)