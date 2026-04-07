from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(200), unique =True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'),)
    password = db.Column(db.String(255) )
    rol = db.relationship('Rol')
    activo = db.Column(db.String(1), default = 'S')
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    
    def __init__(self, nombre:str, email:str, password:str, rol_id:int = 1) -> None:
      self.nombre = nombre
      self.email = email
      self.rol_id = rol_id
      self.password = password
    
    def __repr__(self):
       return f"usuario {self.nombre}, email {self.email} , fecha de creacion {self.created_at} " 
     
    def to_dict(self):
      return {
        'id':self.id,
        'nombre':self.nombre,
        'email':self.email,
        'created_at':self.created_at,
        'updated_at': self.updated_at,
        'rol': self.rol.to_dict() if self.rol else None
      }
      
    def validate_password(self, password:str) -> bool:
      return check_password_hash(self.password, password)
    
    def generate_password(self, password:str):
      self.password = generate_password_hash(password)