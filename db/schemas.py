from pydantic import BaseModel, EmailStr

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True