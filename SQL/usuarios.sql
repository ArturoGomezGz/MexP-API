-- Crear tabla de tipos de usuarios
CREATE TABLE tipo_usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- Insertar tres tipos de usuario: Administrador, Escuela y Aliado
INSERT INTO tipo_usuarios (nombre, descripcion) VALUES
    ('Administrador', 'Usuario con acceso total al sistema.'),
    ('Escuela', 'Entidad educativa con permisos específicos.'),
    ('Aliado', 'Colaborador externo con funciones limitadas.');

-- Crear tabla de usuarios con dirección opcional
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    direccion TEXT NULL,
    tipo_usuario_id INT NOT NULL,
    FOREIGN KEY (tipo_usuario_id) REFERENCES tipo_usuarios(id) ON DELETE CASCADE
);

-- Crear tabla de credenciales para almacenar contraseñas separadas
CREATE TABLE credenciales (
    id SERIAL PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Vista para Administradores: Acceden a todos los usuarios
CREATE VIEW v_administradores AS
SELECT u.id, u.nombre, u.correo, u.direccion, tu.nombre AS tipo_usuario
FROM usuarios u
JOIN tipo_usuarios tu ON u.tipo_usuario_id = tu.id;

-- Vista para Escuelas: Solo ven usuarios de tipo "Escuela"
CREATE VIEW v_escuelas AS
SELECT u.id, u.nombre, u.correo, u.direccion
FROM usuarios u
WHERE u.tipo_usuario_id = (SELECT id FROM tipo_usuarios WHERE nombre = 'Escuela');

-- Vista para Aliados: Solo ven usuarios de tipo "Aliado"
CREATE VIEW v_aliados AS
SELECT u.id, u.nombre, u.correo, u.direccion
FROM usuarios u
WHERE u.tipo_usuario_id = (SELECT id FROM tipo_usuarios WHERE nombre = 'Aliado');

------------------------------------------------------
-- Funciones para gestionar usuarios y credenciales --
------------------------------------------------------

-- Función para insertar un usuario y sus credenciales
CREATE OR REPLACE FUNCTION insertar_usuario(
    p_nombre VARCHAR,
    p_correo VARCHAR,
    p_direccion TEXT,
    p_tipo_usuario_id INT,
    p_password_hash TEXT
) RETURNS VOID AS $$
DECLARE
    v_usuario_id INT;
BEGIN
    -- Insertar el usuario en la tabla usuarios
    INSERT INTO usuarios (nombre, correo, direccion, tipo_usuario_id)
    VALUES (p_nombre, p_correo, p_direccion, p_tipo_usuario_id)
    RETURNING id INTO v_usuario_id;

    -- Insertar la contraseña en la tabla credenciales
    INSERT INTO credenciales (usuario_id, password_hash)
    VALUES (v_usuario_id, p_password_hash);
END;
$$ LANGUAGE plpgsql;

-- Funcion para obtener informacion de un usuario por email
CREATE OR REPLACE FUNCTION obtener_usuario(p_correo VARCHAR)
RETURNS TABLE(id INT, nombre VARCHAR, correo VARCHAR, direccion TEXT, tipo_usuario VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.nombre, u.correo, u.direccion, tu.nombre AS tipo_usuario
    FROM usuarios u
    JOIN tipo_usuarios tu ON u.tipo_usuario_id = tu.id
    WHERE u.correo = p_correo;
END;
$$ LANGUAGE plpgsql;

-- Funcion para cambiar la contrasena de un usuario por email
CREATE OR REPLACE FUNCTION cambiar_contrasena(p_correo VARCHAR, p_nueva_password_hash TEXT)
RETURNS VOID AS $$
DECLARE
    v_usuario_id INT;
BEGIN
    -- Buscar el usuario por correo
    SELECT id INTO v_usuario_id FROM usuarios WHERE correo = p_correo;

    -- Si el usuario existe, actualizar la contrasena
    IF v_usuario_id IS NOT NULL THEN
        UPDATE credenciales SET password_hash = p_nueva_password_hash WHERE usuario_id = v_usuario_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Funcion para obtener la contrasena de un usuario por email
CREATE OR REPLACE FUNCTION obtener_contrasena(p_correo VARCHAR)
RETURNS TEXT AS $$
DECLARE
    v_password_hash TEXT;
BEGIN
    -- Obtener el hash de la contrasena del usuario
    SELECT c.password_hash INTO v_password_hash 
    FROM credenciales c 
    JOIN usuarios u ON c.usuario_id = u.id
    WHERE u.correo = p_correo;

    RETURN v_password_hash;
END;
$$ LANGUAGE plpgsql;