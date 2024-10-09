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

-- Crear la tabla de Libros (ejemplo para referencias futuras)
CREATE TABLE IF NOT EXISTS Libros (
    ID_libro SERIAL PRIMARY KEY,
    Titulo VARCHAR(255) NOT NULL,
    ID_autor INT,
    ISBN VARCHAR(20) UNIQUE,
    Genero VARCHAR(50),
    Fecha_publicacion DATE,
    Numero_paginas INT,
    Editorial VARCHAR(100),
    Idioma VARCHAR(50),
    Resumen TEXT,
    Disponibilidad BOOLEAN DEFAULT TRUE
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

-- Datos de ejemplo para la tabla Clientes
INSERT INTO Clientes (Nombre, Apellido, Fecha_nacimiento, Email, Telefono, Direccion)
VALUES
    ('Juan', 'Pérez', '1990-05-10', 'juan.perez@example.com', '123456789', 'Calle Falsa 123'),
    ('María', 'Gómez', '1985-11-22', 'maria.gomez@example.com', '987654321', 'Avenida Siempre Viva 742'),
    ('Carlos', 'López', '1995-03-15', 'carlos.lopez@example.com', '456789123', 'Boulevard de los Sueños Rotos 56');

-- Datos de ejemplo para la tabla Libros
INSERT INTO Libros (Titulo, ISBN, Genero, Fecha_publicacion, Numero_paginas, Editorial, Idioma, Resumen)
VALUES
    ('El Principito', '978-3-16-148410-0', 'Ficción', '1943-04-06', 96, 'Editorial XYZ', 'Español', 'Una historia sobre la amistad y la soledad.'),
    ('Cien Años de Soledad', '978-3-16-148410-1', 'Ficción', '1967-05-30', 400, 'Editorial ABC', 'Español', 'La historia de la familia Buendía en Macondo.');

-- Datos de ejemplo para la tabla Valoraciones
INSERT INTO Valoraciones (ID_libro, ID_cliente, Puntuacion, Comentario)
VALUES
    (1, 1, 5, 'Una obra maestra, muy recomendada.'),
    (2, 2, 4, 'Una narrativa envolvente.');

-- Datos de ejemplo para la tabla HistorialCliente
INSERT INTO HistorialCliente (ID_cliente, ID_libro)
VALUES
    (1, 1),
    (1, 2),
    (2, 1);
