from app.controllers.user_controller import UserController
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access


users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/')
@jwt_required()
@rol_access(['admin', 'user'])
def get_all():
    return UserController.get_all()
@users.route('/<int:id>')
@jwt_required()
@rol_access(['admin', 'user'])
def show(id):
    return UserController.show(id)

@users.route("/", methods=['POST'])
@jwt_required()
@rol_access(['admin'])
def create():
    return UserController.create(request.get_json())

@users.route("/<int:id>", methods=['PUT'])
@jwt_required()
@rol_access(['admin'])
def update(id):
    return  UserController.update(request=request.get_json(), id=id)
    

@users.route("/<int:id>", methods=['DELETE'])
@jwt_required()
@rol_access(['admin'])
def destroy(id):
    return UserController.destroy( id)
