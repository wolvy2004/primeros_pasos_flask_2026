from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/')
    @app.route('/<nombre>')
    def home(nombre = None):
        if (nombre == None):
            return f' <h1>Hola  desde programacion web dinamica 2026<h1>'
        return f'Hola {nombre} te saludamos desde programacion web dinamica 2026'

    @app.route('/saludo')
    def saludo():
        return f'Hola desde programacion web dinamica 2026 saludo'
    
    return app
    