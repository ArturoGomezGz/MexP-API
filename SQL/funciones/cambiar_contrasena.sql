-- FUNCTION: public.cambiar_contrasena(character varying, text)

-- DROP FUNCTION IF EXISTS public.cambiar_contrasena(character varying, text);

CREATE OR REPLACE FUNCTION public.cambiar_contrasena(
	p_correo character varying,
	p_nueva_password_hash text)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_usuario_id INT;
BEGIN
    -- Buscar el usuario por correo
    SELECT id INTO v_usuario_id FROM usuarios WHERE correo = p_correo;

    -- Si el usuario existe, actualizar la contrasena
    IF v_usuario_id IS NOT NULL THEN
        UPDATE credenciales SET password_hash = p_nueva_password_hash WHERE usuario_id = v_usuario_id;
    END IF;
END;
$BODY$;

ALTER FUNCTION public.cambiar_contrasena(character varying, text)
    OWNER TO postgres;
