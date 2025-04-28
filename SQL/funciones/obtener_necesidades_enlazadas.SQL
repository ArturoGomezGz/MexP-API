CREATE OR REPLACE FUNCTION obtener_necesidades_enlazadas(escuela_id INT)
RETURNS TABLE (
    id INT,
    nombre VARCHAR,
    descripcion TEXT,
    id_escuela INT,
    id_aliado INT,
    completada BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT n.id, n.nombre, n.descripcion, n.id_escuela, n.id_aliado, n.completada
    FROM necesidades AS n
    WHERE n.id_aliado IS NOT NULL
    AND n.id_escuela = escuela_id;
END;
$$ LANGUAGE plpgsql;