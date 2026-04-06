from typing import Literal

from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class UserController (Controller):
    
    @staticmethod
    def get_all() -> tuple[Response, int]:
        usuarios_list = db.session.execute(db.select(User).order_by(db.desc(User.id))).scalars().all()
        if len(usuarios_list) > 0:
            usuarios_to_dict = [usuario.to_dict() for usuario in usuarios_list ]
            return jsonify(usuarios_to_dict), 200 
        return jsonify({"message": 'datos no encontrados'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        usuario = db.session.get(User, id)
        if usuario:
            return jsonify(usuario.to_dict()), 200
        return jsonify({"message": 'usuario no encontrado'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str = request['nombre']
        email:str = request['email']
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if email is None:
            error = 'El email es requerido'
            
        if error is None:
            try:
                user = User(nombre=nombre, email=email, rol_id=1, password='123456')
                db.session.add(user)
                db.session.commit()
                return jsonify({'message': "usuario creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "Usuario ya registrado"}), 409
        return jsonify ({'message': error}), 422
        
        
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre:str = request['nombre']
        email:str = request['email']
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if email is None:
            error = 'El email es requerido'
            
        if error is None:
            usuario = db.session.get(User, id)
            if usuario:
                try:
                    usuario.nombre = nombre
                    usuario.email = email
                    db.session.commit()
                    return jsonify({'message':'usuario modificado con exito'}), 200
                except IntegrityError:
                    error = 'el email o el username ya existen' 
                    return jsonify({'message':error}), 409
            else:     
                error = 'usuario no encontrado'
            
        return jsonify({'message':error}), 404
        
    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        usuario = db.session.get(User, id)
        error = None
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({'message':'el usuario fue eliminado con exito'}), 200
        else:
            error = 'usuario no encontrado'
        return jsonify({'message':error}), 404