from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


# Configuración de la conexión a PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="100.27.62.167",
        database="db_clients",
        user="root",
        password="utec",
        port="8081"
    )
    return conn


### CRUD para la tabla "Clientes" ###

# Obtener todos los clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clientes), 200


# Obtener un cliente por su ID
@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM Clientes WHERE ID_cliente = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if cliente:
        return jsonify(cliente), 200
    return jsonify({'message': 'Cliente no encontrado'}), 404


# Crear un nuevo cliente
@app.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    if not data or not all(key in data for key in ('Nombre', 'Apellido', 'Email')):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Clientes (Nombre, Apellido, Email, Fecha_registro)
        VALUES (%s, %s, %s, NOW())
        RETURNING ID_cliente;
    """, (data['Nombre'], data['Apellido'], data['Email']))
    cliente_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'ID_cliente': cliente_id, 'message': 'Cliente creado exitosamente'}), 201


# Actualizar un cliente existente
@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    if not data or not all(key in data for key in ('Nombre', 'Apellido', 'Email')):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Clientes 
        SET Nombre = %s, Apellido = %s, Email = %s 
        WHERE ID_cliente = %s
    """, (data['Nombre'], data['Apellido'], data['Email'], id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Cliente actualizado exitosamente'}), 200


# Eliminar un cliente
@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clientes WHERE ID_cliente = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Cliente eliminado exitosamente'}), 200


### CRUD para la tabla "Historial_cliente" ###

# Obtener historial de un cliente
@app.route('/clientes/<int:id_cliente>/historial', methods=['GET'])
def get_historial_cliente(id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT h.ID_historial, h.ID_libro, l.Título, h.Fecha_reserva 
        FROM Historial_cliente h 
        JOIN Libros l ON h.ID_libro = l.ID_libro 
        WHERE h.ID_cliente = %s
    """, (id_cliente,))
    historial = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(historial), 200


# Agregar a historial
@app.route('/clientes/<int:id_cliente>/historial', methods=['POST'])
def add_to_historial(id_cliente):
    data = request.get_json()
    if not data or 'ID_libro' not in data:
        return jsonify({"error": "ID_libro es obligatorio"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Historial_cliente (ID_cliente, ID_libro, Fecha_reserva)
        VALUES (%s, %s, NOW())
    """, (id_cliente, data['ID_libro']))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Libro agregado al historial exitosamente'}), 201


### CRUD para la tabla "Valoraciones" ###

# Obtener valoraciones de un cliente
@app.route('/clientes/<int:id_cliente>/valoraciones', methods=['GET'])
def get_valoraciones_cliente(id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT v.ID_valoracion, l.Título, v.Puntuacion 
        FROM Valoraciones v 
        JOIN Libros l ON v.ID_libro = l.ID_libro 
        WHERE v.ID_cliente = %s
    """, (id_cliente,))
    valoraciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(valoraciones), 200


# Crear una nueva valoración
@app.route('/clientes/<int:id_cliente>/valoraciones', methods=['POST'])
def create_valoracion_cliente(id_cliente):
    data = request.get_json()
    if not data or not all(key in data for key in ('ID_libro', 'Puntuacion')):
        return jsonify({"error": "ID_libro y Puntuacion son obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Valoraciones (ID_cliente, ID_libro, Puntuacion)
        VALUES (%s, %s, %s)
    """, (id_cliente, data['ID_libro'], data['Puntuacion']))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Valoración creada exitosamente'}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
