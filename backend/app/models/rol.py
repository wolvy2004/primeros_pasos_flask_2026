from app.models import db

class Rol(db.Model):
    __tablename__="roles"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, unique = True)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    activo = db.Column(db.String(1), default = 'S')
    
    
    def __init__(self, nombre) -> None:
        self.nombre = nombre
        
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    