-- FUNCTION: public.obtener_id_usuario(text)

-- DROP FUNCTION IF EXISTS public.obtener_id_usuario(text);

CREATE OR REPLACE FUNCTION public.obtener_id_usuario(
	p_identificador text)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_id INTEGER;
BEGIN
    -- Buscar el ID del usuario usando el nombre o el correo electrónico
    SELECT id INTO v_id FROM usuarios WHERE nombre = p_identificador OR correo = p_identificador;

    -- Si no se encuentra el usuario, lanzar un error
    IF v_id IS NULL THEN
        RAISE EXCEPTION 'Usuario no encontrado';
    END IF;

    RETURN v_id;
END;
$BODY$;

ALTER FUNCTION public.obtener_id_usuario(text)
    OWNER TO postgres;
