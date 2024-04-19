from fastapi import HTTPException
from sqlalchemy.orm import Session
import db.models as models
import db.schemas as schemas


# Funciones CRUD

# Crear un usuario
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está en uso")
    db_usuario = models.Usuario(nombre=usuario.nombre, email=usuario.email, password=usuario.password)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Obtener un usuario
def obtener_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Obtener un usuario por email
def obtener_usuario_por_email(db: Session, email: str):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario
    

# Obtener todos los usuarios
def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

# Actualizar un usuario
def actualizar_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioBase):
    db_user = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.query(models.Usuario).filter(models.Usuario.id == usuario_id).update(usuario.dict())
    db.commit()
    return db_user

# Eliminar un usuario
def eliminar_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return HTTPException(status_code=200, detail="Usuario eliminado correctamente")
