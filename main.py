import os
from application.database import db
from flask import Flask
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from application import config
from application.config import LocalDevelopmentConfig

app = None

def create_app():
    app = Flask(__name__,template_folder="templates")
    if os.getenv('ENV',"development") == "production":
        raise Exception("Currently no production congif is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from application.controllers import *

if __name__ == '__main__':
    app.secret_key = 'SuperSecretKey'
    app.run()