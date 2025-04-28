CREATE OR REPLACE FUNCTION eliminar_necesidad(id_necesidad INT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM necesidades WHERE id = id_necesidad;
END;
$$ LANGUAGE plpgsql;