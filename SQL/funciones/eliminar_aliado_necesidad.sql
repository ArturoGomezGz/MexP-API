CREATE FUNCTION eliminar_aliado_necesidad(p_id_necesidad INT, p_id_aliado INT) 
RETURNS VOID AS $$
BEGIN
    DELETE FROM necesidades
    WHERE id = p_id_necesidad AND id_aliado = p_id_aliado;
END;
$$ LANGUAGE plpgsql;