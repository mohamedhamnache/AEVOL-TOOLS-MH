from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from Packages.ResourceAlloc import ResourceAlloc

api.add_resource(ResourceAlloc.NodeReservation, '/nodeReservation')
