-- Crear la base de datos
CREATE DATABASE db_clients;

-- Conectarse a la base de datos (esto se debe hacer desde la línea de comandos o desde el cliente de PostgreSQL, no en el script SQL)
USE db_clients;

-- Crear la tabla de Clientes
CREATE TABLE IF NOT EXISTS Clientes (
    ID_cliente SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Fecha_nacimiento DATE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Telefono VARCHAR(15),
    Direccion VARCHAR(255),
    Fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla de Valoraciones
CREATE TABLE IF NOT EXISTS Valoraciones (
    ID_valoracion SERIAL PRIMARY KEY,
    ID_libro INT NOT NULL,
    ID_cliente INT NOT NULL,
    Puntuacion INT CHECK (Puntuacion >= 1 AND Puntuacion <= 5),
    Comentario TEXT,
    Fecha_valoracion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_libro) REFERENCES Libros(ID_libro) ON DELETE CASCADE,
    FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente) ON DELETE CASCADE
);

-- Crear la tabla de HistorialCliente
CREATE TABLE IF NOT EXISTS HistorialCliente (
    ID_historial SERIAL PRIMARY KEY,
    ID_cliente INT NOT NULL,
    ID_libro INT NOT NULL,
    Fecha_lectura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente) ON DELETE CASCADE,
    FOREIGN KEY (ID_libro) REFERENCES Libros(ID_libro) ON DELETE CASCADE
);

