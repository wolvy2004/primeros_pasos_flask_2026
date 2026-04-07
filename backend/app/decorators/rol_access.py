from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models import db
from app.models.user import User
from flask import jsonify

def rol_access(roles_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
            if user and user.rol and user.rol.nombre in roles_permitidos:
                return func(*args, **kwargs)
            return jsonify({'message': 'Acceso denegado: rol no autorizado'}), 403
        return wrapper
    return decorator
