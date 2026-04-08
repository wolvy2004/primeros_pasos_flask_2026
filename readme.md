# Trabajo Práctico N° 1 — Sistema de Gestión de Stock

**Materia:** Programación Web Dinámica  
**Modalidad:** Individual  
**Entorno:** Docker Compose · Flask · PostgreSQL · Python 3.11+  
**Entrega:** Push a la rama `main` de este repositorio

---

> Este trabajo integra los temas vistos hasta la fecha: modelos con SQLAlchemy, Blueprints, controladores, JWT y decoradores de autorización por rol. Todos esos componentes ya los tienen explicados y con ejemplos en clase. La idea es aplicarlos en un dominio nuevo.

---

## Contexto

Tienen que construir el **backend completo** de un sistema de gestión de stock para un pequeño comercio. El sistema permite manejar **categorías**, **productos**, **proveedores** y **movimientos de stock** (entradas y salidas de mercadería).

Hay dos tipos de usuario: `admin` y `operador`, con distintos permisos sobre las rutas.

### Casos de uso

- **Admin:** puede crear, editar y eliminar categorías, productos y proveedores. También puede ver todos los movimientos registrados.
- **Operador:** puede consultar productos y registrar movimientos de entrada o salida.
- **Cualquier usuario autenticado:** puede ver su perfil en `GET /auth/me`.
- **Rutas públicas:** solo `POST /auth/login` y `POST /auth/register`.

---

## Modelos

El sistema tiene cuatro modelos que heredan de su `BaseModel` (con `id`, `created_at`, `updated_at` y `__abstract__ = True`):

### Categoria

| Campo       | Tipo        | Restricciones    |
|-------------|-------------|------------------|
| nombre      | String(100) | not null, unique |
| descripcion | Text        | nullable         |

### Proveedor

| Campo    | Tipo        | Restricciones |
|----------|-------------|---------------|
| nombre   | String(150) | not null      |
| contacto | String(100) | nullable      |
| telefono | String(30)  | nullable      |
| email    | String(120) | nullable      |

### Producto

| Campo        | Tipo                                  | Restricciones |
|--------------|---------------------------------------|---------------|
| nombre       | String(150)                           | not null      |
| descripcion  | Text                                  | nullable      |
| precio_costo | Numeric(10,2)                         | not null      |
| precio_venta | Numeric(10,2)                         | not null      |
| stock_actual | Integer                               | default 0     |
| stock_minimo | Integer                               | default 0     |
| categoria_id | Integer, ForeignKey('categorias.id')  | not null      |
| proveedor_id | Integer, ForeignKey('proveedores.id') | nullable      |

### MovimientoStock

| Campo       | Tipo                                | Restricciones                      |
|-------------|-------------------------------------|------------------------------------|
| tipo        | String(10)                          | `'entrada'` o `'salida'`, not null |
| cantidad    | Integer                             | not null, mayor a 0                |
| motivo      | String(200)                         | nullable                           |
| producto_id | Integer, ForeignKey('productos.id') | not null                           |
| user_id     | Integer, ForeignKey('users.id')     | not null                           |

### Relaciones entre modelos

```
Categoria ──< Producto >── Proveedor
               │
               └──< MovimientoStock >── User
```

> **Atención:** cuando se registra un movimiento de tipo `'entrada'` hay que sumar la cantidad a `stock_actual`. Para `'salida'` hay que restar. Una salida no puede dejar el stock en negativo — tienen que validarlo y devolver un error descriptivo.

---

## Módulo de autenticación

El módulo `auth` ya lo tienen como referencia de clase. Para este TP deben adaptarlo e incluir:

| Método | Ruta           | Descripción                                      |
|--------|----------------|--------------------------------------------------|
| POST   | /auth/register | Crea un usuario con rol `operador` por defecto   |
| POST   | /auth/login    | Devuelve un `access_token` con el rol como claim |
| GET    | /auth/me       | Devuelve el perfil del usuario autenticado       |

> Los modelos `User` y `Rol` de clase siguen siendo válidos. Solo asegúrense de que el claim `'rol'` esté incluido en el token JWT para que el decorador pueda leerlo.

---

## Rutas por Blueprint

El proyecto debe tener al menos **cuatro Blueprints** además de `auth`.

### /categorias

| Método | Ruta              | Descripción        | Rol requerido |
|--------|-------------------|--------------------|---------------|
| GET    | /categorias/      | Listar categorías  | Autenticado   |
| GET    | /categorias/\<id> | Ver una categoría  | Autenticado   |
| POST   | /categorias/      | Crear categoría    | admin         |
| PUT    | /categorias/\<id> | Editar categoría   | admin         |
| DELETE | /categorias/\<id> | Eliminar categoría | admin         |

### /proveedores

| Método | Ruta               | Descripción        | Rol requerido |
|--------|--------------------|--------------------|---------------|
| GET    | /proveedores/      | Listar proveedores | admin         |
| GET    | /proveedores/\<id> | Ver proveedor      | admin         |
| POST   | /proveedores/      | Crear proveedor    | admin         |
| PUT    | /proveedores/\<id> | Editar proveedor   | admin         |
| DELETE | /proveedores/\<id> | Eliminar proveedor | admin         |

### /productos

| Método | Ruta             | Descripción                               | Rol requerido |
|--------|------------------|-------------------------------------------|---------------|
| GET    | /productos/      | Listar productos                          | Autenticado   |
| GET    | /productos/\<id> | Ver producto con su categoría y proveedor | Autenticado   |
| POST   | /productos/      | Crear producto                            | admin         |
| PUT    | /productos/\<id> | Editar producto                           | admin         |
| DELETE | /productos/\<id> | Eliminar producto                         | admin         |

### /movimientos

| Método | Ruta              | Descripción                                 | Rol requerido |
|--------|-------------------|---------------------------------------------|---------------|
| GET    | /movimientos/     | Listar todos los movimientos                | admin         |
| GET    | /movimientos/mis/ | Ver los movimientos del usuario autenticado | Autenticado   |
| POST   | /movimientos/     | Registrar un movimiento de entrada o salida | Autenticado   |

> **Atención:** para `DELETE /categorias/<id>` y `DELETE /proveedores/<id>`, si la entidad tiene productos asociados deben devolver `409 Conflict` con un mensaje descriptivo. No es necesario implementar soft-delete ni eliminación en cascada.

---

## Estructura de carpetas esperada

```
app/
├── __init__.py              # create_app, registrar blueprints y JWT
├── config.py                # clase Config con variables de entorno
├── database.py              # instancia db = SQLAlchemy()
├── models/
│   ├── base_model.py        # BaseModel con __abstract__ = True
│   ├── rol.py
│   ├── user.py
│   ├── categoria.py
│   ├── proveedor.py
│   ├── producto.py
│   └── movimiento_stock.py
├── decorators/
|   |-rol_access.py
├── auth/
│   ├── __init__.py
│   ├── controller.py
├── controllers/
│   ├── __init__.py
│   ├── rol_controller.py
│   ├── user_controller.py
│   ├── auth_controller.py
│   ├── categoria_controller.py
│   ├── proveedor_controller.py
│   ├── producto_controller.py
|   └── movimiento_stock_controller.py
migrations/                  # generado por flask db init — subir al repo
docker-compose.yml
.env
.env-dist
.gitignore
requirements.txt
run.py
README.md
```

---

## Configuración Docker

El proyecto tiene que levantar con un solo comando: `docker-compose up --build`.

El `docker-compose.yml` debe definir **tres servicios**:

- **backend:** la aplicación Flask con hot-reload, montando el código como volumen.
- **db:** PostgreSQL 15 con las variables de entorno del `.env`.
- **pgadmin:** gestor visual de la base de datos. Permite inspeccionar tablas, datos y relaciones durante el desarrollo.

### Variables de entorno (`.env`)

```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1

DATABASE_URL=postgresql://user:password@db:5432/stockdb
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=stockdb

JWT_SECRET_KEY=cambiar-esta-clave
JWT_ACCESS_TOKEN_EXPIRES=3600

PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

> **Importante:** el `.env` no debe subirse al repositorio. El `.gitignore` debe excluir `.env` y `__pycache__/`. Incluyan un `.env.example` con los nombres de las variables sin valores sensibles.

---

## Migraciones con Flask-Migrate

En este proyecto **no usamos `db.create_all()`** directamente. En cambio usamos **Flask-Migrate**, que genera migraciones a partir de los modelos y las aplica sobre la base de datos. Esto permite llevar un historial de cambios en el esquema.

Los comandos básicos, ejecutados dentro del contenedor `backend`:

```bash
# Solo la primera vez: inicializar la carpeta de migraciones
flask db init

# Cada vez que modifican un modelo: generar la migración
flask db migrate -m "descripcion del cambio"

# Aplicar las migraciones pendientes a la base de datos
flask db upgrade
```

La carpeta `migrations/` que genera `flask db init` **debe subirse al repositorio** — es parte del proyecto.

> Para que Flask-Migrate detecte los modelos, todos tienen que estar importados en el contexto de la app antes de correr `flask db migrate`. Revisen que en `create_app` estén importando los modelos.

---

## Seed — datos iniciales

El seeder es un script que inserta datos de prueba en la base de datos para poder probar el sistema sin cargar todo a mano. **Es un tema que todavía no vimos en clase**, pero no es difícil de implementar y les va a ahorrar mucho tiempo.

Una forma simple es crear un archivo `seeder.py` en la raíz del proyecto:

```python
# seed.py
from app import create_app
from app.database import db
from app.models.rol import Rol
from app.models.user import User
from app.models.categoria import Categoria
from app.models.proveedor import Proveedor
from app.models.producto import Producto

app = create_app()

with app.app_context():
    # Roles
    rol_admin = Rol(nombre='admin')
    rol_op    = Rol(nombre='operador')
    db.session.add_all([rol_admin, rol_op])
    db.session.commit()

    # Usuario admin
    admin = User(username='admin', email='admin@stock.com', rol=rol_admin)
    admin.generate_password('admin123')
    db.session.add(admin)

    # Categorías
    alm = Categoria(nombre='Almacén', descripcion='Productos secos')
    lim = Categoria(nombre='Limpieza', descripcion='Artículos de limpieza')
    db.session.add_all([alm, lim])

    # Proveedor
    prov = Proveedor(nombre='Distribuidora Norte', telefono='2994001234')
    db.session.add(prov)
    db.session.commit()

    # Productos
    db.session.add_all([
        Producto(nombre='Harina 000', precio_costo=280, precio_venta=350,
                 stock_actual=50, stock_minimo=10,
                 categoria_id=alm.id, proveedor_id=prov.id),
        Producto(nombre='Lavandina 1L', precio_costo=150, precio_venta=210,
                 stock_actual=30, stock_minimo=5,
                 categoria_id=lim.id, proveedor_id=prov.id),
    ])
    db.session.commit()
    print("Seed completado.")
```

Para ejecutarlo dentro del contenedor:

```bash
docker-compose exec backend python seed.py
```


---

## Respuestas JSON esperadas

Todas las respuestas deben ser JSON.

**Listado de productos (`GET /productos/`):**
```json
[
  {
    "id": 1,
    "nombre": "Harina 000",
    "precio_venta": "350.00",
    "stock_actual": 50,
    "stock_minimo": 10,
    "categoria": { "id": 1, "nombre": "Almacén" },
    "proveedor": { "id": 1, "nombre": "Distribuidora Norte" }
  }
]
```

**Error de negocio:**
```json
{ "error": "Stock insuficiente para registrar la salida" }
```

**Error de autorización:**
```json
{ "msg": "Acceso denegado: se requiere rol admin" }
```

---

## Fragmentos de referencia

### Decorador de roles (este es diferente al que creamos pero usa el jwt y no accede a la base de datos)

```python
# auth/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def rol_access(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # verifica que tenga el token en el request, el get_jwt toma los datos del mismo 
            # busca que tenga el claim "rol" 
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("rol") not in roles:
                return jsonify(
                    msg=f"Acceso denegado: se requiere rol {' o '.join(roles)}"
                ), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
```


## Orden sugerido de implementación

Si no saben por dónde arrancar, este orden les va a ahorrar tiempo:

1. Crear `BaseModel` y luego los modelos: `Rol` → `User` → `Categoria` → `Proveedor` → `Producto` → `MovimientoStock`.
Pueden crear los modelos como venimos haciendo,sin el BaseModel, esta parte la explico el viernes 09/04/2026.
2. Correr `flask db init`, `flask db migrate` y `flask db upgrade`. o correr el `firt_step.sh` Verificar las tablas en pgadmin. 
3. Implementar el módulo `auth` completo. Probar register y login.
4. Implementar el Blueprint de `categorias` (el más simple). Probar GET, POST, PUT, DELETE con el token.
5. Implementar `proveedores` (misma estructura que categorías).
6. Implementar `productos` con las relaciones en la respuesta.
7. Implementar `movimientos` con la lógica de actualización de stock.

---

## Cómo se evalúa

No hay nota numérica — este TP es una ejercitación. Se va a revisar que:

- Los cuatro modelos están implementados con sus relaciones correctas
- Las migraciones están presentes y el esquema se crea con `flask db upgrade`
- El login devuelve un JWT con el claim `rol`
- El decorador `@rol_requerido` protege las rutas correctamente
- Registrar un movimiento actualiza el `stock_actual` del producto
- Una salida con cantidad mayor al stock actual devuelve error
- El sistema levanta con `docker-compose up --build` sin errores

> Si el sistema no levanta con Docker no se puede revisar el resto. Prueben el flujo completo antes de hacer el push final.
