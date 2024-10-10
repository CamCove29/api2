from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.responses import JSONResponse
import httpx
app = FastAPI()

def get_db_connection():
    conn = psycopg2.connect(
        host="3.85.121.200",
        database="db_clients",
        user="root",
        password="utec",
        port="8006"
    )
    return conn

# Modelo para los datos de un cliente
class Cliente(BaseModel):
    ID_cliente: int  # Campo obligatorio
    Nombre: str
    Apellido: str
    Fecha_nacimiento: str  # Utiliza formato ISO para fechas (YYYY-MM-DD)
    Email: str
    Telefono: str  # Campo obligatorio
    Direccion: str  # Campo obligatorio
    Fecha_registro: datetime  # Campo obligatorio

# Modelo para el historial de un cliente
class Historial(BaseModel):
    ID_historial: int  # Campo obligatorio
    ID_cliente: int  # Campo obligatorio
    ID_libro: int  # Campo obligatorio
    Fecha_lectura: datetime  # Campo obligatorio, generado automáticamente

# Modelo para las valoraciones de un cliente
class Valoracion(BaseModel):
    ID_valoracion: int  # Campo obligatorio
    ID_libro: int  # Campo obligatorio
    ID_cliente: int  # Campo obligatorio
    Puntuacion: int  # Asegúrate de que esté entre 1 y 5
    Comentario: str  # Campo obligatorio
    Fecha_valoracion: datetime  # Campo obligatorio, generado automáticamente


# Get echo test for load balancer's health check
@app.get("/")
def get_echo_test():
    return {"message": "Echo Test OK"}


# Obtener todos los clientes
@app.get("/clientes")
def get_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=clientes)


# Obtener un cliente por su ID
@app.get("/clientes/{id_cliente}")
def get_cliente(id_cliente: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Clientes WHERE ID_cliente = %s", (id_cliente,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if cliente:
        return JSONResponse(content=cliente)
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


# Crear un nuevo cliente
@app.post("/clientes", response_model=dict)
def create_cliente(cliente: Cliente):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Clientes (Nombre, Apellido, Email, Telefono, Direccion, Fecha_nacimiento, Fecha_registro)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
        RETURNING ID_cliente;
    """, (
    cliente.Nombre, cliente.Apellido, cliente.Email, cliente.Telefono, cliente.Direccion, cliente.Fecha_nacimiento))
    cliente_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return {"ID_cliente": cliente_id, "message": "Cliente creado exitosamente"}


# Actualizar un cliente existente
@app.put("/clientes/{id_cliente}", response_model=dict)
def update_cliente(id_cliente: int, cliente: Cliente):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Clientes 
        SET Nombre = %s, Apellido = %s, Email = %s, Telefono = %s, Direccion = %s, Fecha_nacimiento = %s 
        WHERE ID_cliente = %s
    """, (
    cliente.Nombre, cliente.Apellido, cliente.Email, cliente.Telefono, cliente.Direccion, cliente.Fecha_nacimiento,
    id_cliente))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Cliente actualizado exitosamente"}


# Eliminar un cliente
@app.delete("/clientes/{id_cliente}", response_model=dict)
def delete_cliente(id_cliente: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clientes WHERE ID_cliente = %s", (id_cliente,))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Cliente eliminado exitosamente"}


# URL base de la API de libros
LIBROS_API_URL = "http://3.85.121.200:8005"


# Obtener historial de un cliente
@app.get("/clientes/{id_cliente}/historial")
def get_historial_cliente(id_cliente: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT h.ID_historial, h.ID_libro, l.Titulo, h.Fecha_reserva 
        FROM Historial_cliente h 
        JOIN Libros l ON h.ID_libro = l.ID_libro 
        WHERE h.ID_cliente = %s
    """, (id_cliente,))
    historial = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=historial)


# Agregar a historial
@app.post("/clientes/{id_cliente}/historial")
async def add_to_historial(id_cliente: int, historial: Historial):
    # Llamada a la API de libros para obtener el ID_libro
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LIBROS_API_URL}/libros/{historial.ID_libro}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Libro no encontrado en la API de libros")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Historial_cliente (ID_cliente, ID_libro, Fecha_reserva)
        VALUES (%s, %s, NOW())
    """, (id_cliente, historial.ID_libro))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Libro agregado al historial exitosamente"}


# Obtener valoraciones de un cliente
@app.get("/clientes/{id_cliente}/valoraciones")
def get_valoraciones_cliente(id_cliente: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT v.ID_valoracion, l.Titulo, v.Puntuacion 
        FROM Valoraciones v 
        JOIN Libros l ON v.ID_libro = l.ID_libro 
        WHERE v.ID_cliente = %s
    """, (id_cliente,))
    valoraciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return JSONResponse(content=valoraciones)


# Crear una nueva valoración
@app.post("/clientes/{id_cliente}/valoraciones")
async def create_valoracion_cliente(id_cliente: int, valoracion: Valoracion):
    # Llamada a la API de libros para obtener el ID_libro
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LIBROS_API_URL}/libros/{valoracion.ID_libro}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Libro no encontrado en la API de libros")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Valoraciones (ID_cliente, ID_libro, Puntuacion)
        VALUES (%s, %s, %s)
    """, (id_cliente, valoracion.ID_libro, valoracion.Puntuacion))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Valoración creada exitosamente"}
