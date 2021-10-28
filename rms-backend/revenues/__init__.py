import logging
import os

from flask import Flask, Blueprint, request
from flask_compress import Compress
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.engine import create_engine

from config import RmsConfig

compress = Compress()
db = SQLAlchemy()
engine = create_engine(RmsConfig.SQLALCHEMY_DATABASE_URI)
TOP_DIR = os.path.dirname(__file__) or "."
migrate = Migrate()
logger_format = "%(asctime)s %(filename)s:%(lineno)d:%(levelname)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=logger_format)
logger = logging.getLogger(__name__)
blueprint = Blueprint('api', __name__)
api = Api(blueprint)

from revenues.main.views import main
from revenues.expense.views import expense
from revenues.revenue.views import revenue


def create_app():
    app = Flask(__name__)
    app.config.from_object(RmsConfig)
    compress.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    app.url_map.redirect_defaults = False

    app.register_blueprint(blueprint)
    api.add_namespace(main)
    api.add_namespace(expense)
    api.add_namespace(revenue)

    return app


@api.errorhandler
def handle_exception(error: Exception):
    import traceback
    """When an unhandled exception is raised"""
    logger.warning('Handle internal server error start...')
    url, method = request.url, request.method
    message = "Error: " + getattr(error, 'message', str(error))
    traceback = traceback.format_exc()
    logger.warning(url)
    logger.warning(method)
    logger.warning(message)
    logger.warning(traceback)
    return {"status": "failure", "message": "系统异常"}, getattr(error, 'code', 500)
