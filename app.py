from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from config2 import Config2

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config2)

    db.init_app(app)
    migrate.init_app(app, db)

    from model import Car, Pet, Fruits

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True,port=9000)