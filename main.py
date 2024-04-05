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