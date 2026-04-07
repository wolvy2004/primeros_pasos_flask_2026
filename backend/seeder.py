from flask_sqlalchemy import SQLAlchemy
from app.models.user import User
from app.models.rol import Rol
from app.models import db
from flask import Flask
from app import create_app

app = create_app()


def seed():
    # Crear roles
    admin_role = Rol(nombre='superadmin')
    user_role = Rol(nombre='user')
    db.session.add_all([admin_role, user_role])
    db.session.commit()

    # Crear usuarios
    admin_user = User(nombre='admin', password='admin123', rol_id=admin_role.id, email='admin@example.com')
    regular_user = User(nombre='user', password='user123', rol_id=user_role.id, email='user@example.com')
    db.session.add_all([admin_user, regular_user])
    db.session.commit()
    
if __name__ == '__main__':
    with app.app_context():
        seed()