CREATE OR REPLACE FUNCTION public.set_descripcion_usuario(
    p_correo TEXT,
    p_descripcion TEXT
) RETURNS VOID AS
$$
DECLARE
    v_id INTEGER;
BEGIN
    -- Obtener el ID del usuario basado en el correo
    SELECT obtener_id_usuario(p_correo) INTO v_id;

    -- Actualizar la descripción solo si encontramos un usuario
    IF v_id IS NOT NULL THEN
        UPDATE usuarios
        SET descripcion = p_descripcion
        WHERE id = v_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

ALTER FUNCTION public.set_descripcion_usuario(TEXT, TEXT)
    OWNER TO postgres;