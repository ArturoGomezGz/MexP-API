CREATE OR REPLACE FUNCTION obtener_necesidades(id_usuario INT)
RETURNS TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    id_escuela INT,
    id_aliado INT,
    completada BOOLEAN
) AS
$$
BEGIN
    RETURN QUERY
    SELECT n.id, n.nombre, n.descripcion, n.id_escuela, n.id_aliado, n.completada
    FROM necesidades n
    WHERE n.id_escuela = id_usuario;
END;
$$ LANGUAGE plpgsql;