from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, date  # Asegúrate de importar 'date' aquí
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.responses import JSONResponse

app = FastAPI()

def get_db_connection():
    conn = psycopg2.connect(
        host="98.81.251.98",
        database="db_clients",
        user="root",
        password="utec",
        port="8010"
    )
    return conn

class Usuario(BaseModel):
    ID: int  # Opcional si es autogenerado
    nombre_usuario: str
    correo_electronico: str
    contraseña: str

class DatosUsuario(BaseModel):
    ID_usuario: int  # Referencia al ID del usuario
    nombres: str
    apellidos: str
    numero_telefono: str
    edad: int
    direccion: str # Aquí se puede usar 'date' ya que fue importado

# Get echo test for load balancer's health check
@app.get("/")
def get_echo_test():
    return {"message": "Echo Test OK"}

# Obtener todos los usuarios
@app.get("/usuarios")
def get_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=usuarios)

# Obtener un usuario por su ID
@app.get("/usuarios/{user_id}")
def get_usuario(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Usuarios WHERE ID = %s", (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if usuario:
        return JSONResponse(content=usuario)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Crear un nuevo usuario
@app.post("/usuarios")
def create_usuario(usuario: Usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Usuarios (nombre_usuario, correo_electronico, contraseña)
        VALUES (%s, %s, %s)
        RETURNING ID;
    """, (usuario.nombre_usuario, usuario.correo_electronico, usuario.contraseña))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"ID": user_id, "message": "Usuario creado exitosamente"}

# Actualizar un usuario
@app.put("/usuarios/{user_id}")
def update_usuario(user_id: int, usuario: Usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Usuarios 
        SET nombre_usuario = %s, correo_electronico = %s, contraseña = %s 
        WHERE ID = %s
    """, (usuario.nombre_usuario, usuario.correo_electronico, usuario.contraseña, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Usuario actualizado exitosamente"}

# Eliminar un usuario
@app.delete("/usuarios/{user_id}")
def delete_usuario(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Usuarios WHERE ID = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Usuario eliminado exitosamente"}

# CRUD para la tabla Datos_Usuario

# Obtener datos del usuario
@app.get("/usuarios/{user_id}/datos")
def get_datos_usuario(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Datos_Usuario WHERE ID_usuario = %s", (user_id,))
    datos = cursor.fetchone()
    cursor.close()
    conn.close()
    if datos:
        return JSONResponse(content=datos)
    raise HTTPException(status_code=404, detail="Datos del usuario no encontrados")

# Crear datos de usuario
@app.post("/usuarios/{user_id}/datos")
def create_datos_usuario(user_id: int, datos_usuario: DatosUsuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Datos_Usuario (ID_usuario, nombres, apellidos, numero_telefono, edad, direccion)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        user_id, datos_usuario.nombres, datos_usuario.apellidos, 
        datos_usuario.numero_telefono, datos_usuario.edad, datos_usuario.direccion))  # Actualiza aquí
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Datos del usuario creados exitosamente"}

# Actualizar datos de usuario
@app.put("/usuarios/{user_id}/datos")
def update_datos_usuario(user_id: int, datos_usuario: DatosUsuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Datos_Usuario 
        SET nombres = %s, apellidos = %s, numero_telefono = %s, edad = %s, direccion = %s
        WHERE ID_usuario = %s
    """, (
        datos_usuario.nombres, datos_usuario.apellidos, datos_usuario.numero_telefono, 
        datos_usuario.edad, datos_usuario.direccion, user_id))  # Actualiza aquí
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Datos del usuario actualizados exitosamente"}

# Eliminar datos de usuario
@app.delete("/usuarios/{user_id}/datos")
def delete_datos_usuario(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Datos_Usuario WHERE ID_usuario = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
  
