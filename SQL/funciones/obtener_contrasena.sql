-- FUNCTION: public.obtener_contrasena(character varying)

-- DROP FUNCTION IF EXISTS public.obtener_contrasena(character varying);

CREATE OR REPLACE FUNCTION public.obtener_contrasena(
	p_correo character varying)
    RETURNS text
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_password_hash TEXT;
BEGIN
    -- Obtener el hash de la contrasena del usuario
    SELECT c.password_hash INTO v_password_hash 
    FROM credenciales c 
    JOIN usuarios u ON c.usuario_id = u.id
    WHERE u.correo = p_correo;

    RETURN v_password_hash;
END;
$BODY$;

ALTER FUNCTION public.obtener_contrasena(character varying)
    OWNER TO postgres;
