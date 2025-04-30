CREATE OR REPLACE FUNCTION eliminar_necesidad(p_id_necesidad INT)
RETURNS TABLE(resultado TEXT) AS $$
BEGIN
    DELETE FROM relacion_aliado_necesidad WHERE id_necesidad = p_id_necesidad;
    DELETE FROM necesidades WHERE id = p_id_necesidad;
    RETURN QUERY SELECT 'ok';
END;
$$ LANGUAGE plpgsql;