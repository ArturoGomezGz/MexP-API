CREATE OR REPLACE FUNCTION obtener_necesidades_enlazadas_escuela(
    p_correo TEXT
) RETURNS TABLE (
    id INTEGER,
    nombre VARCHAR(100),
    descripcion TEXT,
    id_escuela INTEGER,
    id_aliado INTEGER,
    completada BOOLEAN
) AS
$$
DECLARE
    v_id_escuela INTEGER;
BEGIN
    -- Obtener el ID de la escuela basado en su correo
    SELECT obtener_id_usuario(p_correo) INTO v_id_escuela;

    -- Ejecutar la consulta solo si encontramos una escuela
    IF v_id_escuela IS NOT NULL THEN
        RETURN QUERY
        SELECT n.id, n.nombre, n.descripcion, n.id_escuela, n.id_aliado, n.completada
        FROM necesidades AS n
        WHERE n.id_escuela = v_id_escuela
        AND n.id_aliado IS NOT NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;