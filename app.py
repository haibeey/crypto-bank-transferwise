from flask import Blueprint
from flask_restful import Api
import logging
from utils import catchExceptions
from api.apis import MakeTransfer

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route


@api_bp.route("/")
@catchExceptions
def home():
    return "hello world"

api.add_resource(MakeTransfer, '/make/transfer/')