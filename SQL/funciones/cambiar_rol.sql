-- FUNCTION: public.cambiar_rol(character varying, integer)

-- DROP FUNCTION IF EXISTS public.cambiar_rol(character varying, integer);

CREATE OR REPLACE FUNCTION public.cambiar_rol(
	p_correo character varying,
	p_nuevo_tipo_usuario_id integer)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_usuario_id INT;
BEGIN
    -- Obtener el ID del usuario basado en su correo
    SELECT id INTO v_usuario_id FROM usuarios WHERE correo = p_correo;

    -- Si el usuario existe, actualizar su tipo de usuario
    IF v_usuario_id IS NOT NULL THEN
        UPDATE usuarios SET tipo_usuario_id = p_nuevo_tipo_usuario_id WHERE id = v_usuario_id;
    END IF;
END;
$BODY$;

ALTER FUNCTION public.cambiar_rol(character varying, integer)
    OWNER TO postgres;
