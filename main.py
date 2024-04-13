from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from db.config import engine, SessionLocal
import db.models
import db.crud as crud
import db.schemas as schemas
from jwt_manager.jwt_config import create_token, verify_token
from fastapi.security import HTTPBearer

db.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = verify_token(auth.credentials)
        db = SessionLocal()
        user = crud.obtener_usuario_por_email(db, data['email'])
        if data['email'] != user.email:
            return HTTPException(status_code=403, detail="Credenciales no son validas")

@app.get("/")
def main():
    return {"Hello": "World"}




@app.post("/login", tags=["login"])
def login(usuario: schemas.UsuarioLogin):
    db = SessionLocal()
    usuario_db = crud.obtener_usuario_por_email(db, usuario.email)
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario_db.password != usuario.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    token = create_token(usuario.dict())
    return JSONResponse(content={"token": token}, status_code=200)

# ruta para crear un usuario
@app.post("/crear_usuario")
def crear_usuario(usuario: schemas.UsuarioCreate):
    db = SessionLocal()
    usuario_creado = crud.crear_usuario(db, usuario)
    return usuario_creado, HTTPException(status_code=201, detail="Usuario creado correctamente")

# ruta para obtener un usuario
@app.get("/obtener_usuario/{usuario_id}")
def  obtener_usuario(usuario_id: int):
    db = SessionLocal()
    usuario_id = crud.obtener_usuario(db, usuario_id)
    if not usuario_id:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_id, HTTPException(status_code=200, detail="Usuario encontrado")

# ruta para obtener todos los usuarios
@app.get("/obtener_usuarios", dependencies=[Depends(JWTBearer())])
def obtener_usuarios(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    usurios = crud.obtener_usuarios(db, skip, limit)
    return usurios, HTTPException(status_code=200, detail="Usuarios encontrados")

# ruta para actualizar un usuario
@app.put("/actualizar_usuario/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioBase):
    db = SessionLocal()
    usuario_edit = crud.actualizar_usuario(db, usuario_id, usuario)
    if not usuario_edit:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return HTTPException(status_code=200, detail="Usuario actualizado correctamente")

# ruta para eliminar un usuario
@app.delete("/eliminar_usuario/{usuario_id}", response_model=schemas.UsuarioBase)
def eliminar_usuario(usuario_id: int):
    db = SessionLocal()
    crud.eliminar_usuario(db, usuario_id)
    return HTTPException(status_code=200, detail="Usuario eliminado correctamente")

# ruta para obtener un usuario por email
@app.get("/obtener_usuario_por_email", response_model=schemas.UsuarioBase)
def obtener_usuario_por_email(email: str):
    db = SessionLocal()
    return crud.obtener_usuario_por_email(db, email)

