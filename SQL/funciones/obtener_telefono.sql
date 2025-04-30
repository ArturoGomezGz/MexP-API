CREATE FUNCTION obtener_telefono(id_usuario INT) 
RETURNS TABLE(telefono VARCHAR(20)) AS $$
BEGIN
    RETURN QUERY 
    SELECT numero AS telefono 
    FROM usuarios 
    WHERE id = id_usuario;
END;
$$ LANGUAGE plpgsql;