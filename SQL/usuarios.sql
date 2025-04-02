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