from fastapi import FastAPI, HTTPException, Depends
from db.config import engine, SessionLocal
import db.models
import db.crud as crud
import db.schemas as schemas

db.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def main():
    return {"Hello": "World"}

@app.post("/crear_usuario")
def crear_usuario(usuario: schemas.UsuarioCreate):
    db = SessionLocal()
    return crud.crear_usuario(db, usuario)

@app.get("/obtener_usuario/{usuario_id}")
def obtener_usuario(usuario_id: int):
    db = SessionLocal()
    return crud.obtener_usuario(db, usuario_id)

@app.get("/obtener_usuarios")
def obtener_usuarios(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    return crud.obtener_usuarios(db, skip, limit)

@app.put("/actualizar_usuario/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioBase):
    db = SessionLocal()
    return crud.actualizar_usuario(db, usuario_id, usuario)

@app.delete("/eliminar_usuario/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    db = SessionLocal()
    return crud.eliminar_usuario(db, usuario_id)

@app.get("/obtener_usuario_por_email")
def obtener_usuario_por_email(email: str):
    db = SessionLocal()
    return crud.obtener_usuario_por_email(db, email)

