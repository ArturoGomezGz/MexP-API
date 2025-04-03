-- Crear tabla de tipos de necesidad
CREATE TABLE tipo_necesidad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Crear tabla de necesidades
CREATE TABLE necesidades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    id_escuela INT NOT NULL,
    id_aliado INT NULL,
    FOREIGN KEY (id_escuela) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (id_aliado) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Crear tabla que relaciona las necesidades con diferentes tipos de necesidad
CREATE TABLE relacion_necesidad_tipo (
    id_relacion SERIAL PRIMARY KEY,
    id_tipo_necesidad INT NOT NULL,
    id_necesidad INT NOT NULL,
    FOREIGN KEY (id_tipo_necesidad) REFERENCES tipo_necesidad(id) ON DELETE CASCADE,
    FOREIGN KEY (id_necesidad) REFERENCES necesidades(id) ON DELETE CASCADE
);

-- Crear tabla que relaciona los tipos de necesidad con aliados
CREATE TABLE relacion_aliado_tipo (
    id_relacion SERIAL PRIMARY KEY,
    id_tipo_necesidad INT NOT NULL,
    id_aliado INT NOT NULL,
    FOREIGN KEY (id_tipo_necesidad) REFERENCES tipo_necesidad(id) ON DELETE CASCADE,
    FOREIGN KEY (id_aliado) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Funcion para crear una necesidad
CREATE OR REPLACE FUNCTION crear_necesidad(
    p_nombre VARCHAR,
    p_descripcion TEXT,
    p_id_escuela INT,
    p_id_aliado INT DEFAULT NULL
) RETURNS VOID AS $$
BEGIN
    INSERT INTO necesidades (nombre, descripcion, id_escuela, id_aliado)
    VALUES (p_nombre, p_descripcion, p_id_escuela, p_id_aliado);
END;
$$ LANGUAGE plpgsql;