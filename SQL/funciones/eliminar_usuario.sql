-- FUNCTION: public.eliminar_usuario(character varying)

-- DROP FUNCTION IF EXISTS public.eliminar_usuario(character varying);

CREATE OR REPLACE FUNCTION public.eliminar_usuario(
	p_correo character varying)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_usuario_id INT;
BEGIN
    -- Obtener el ID del usuario basado en su correo electrónico
    SELECT id INTO v_usuario_id FROM usuarios WHERE correo = p_correo;

    -- Si el usuario existe, eliminar sus registros relacionados
    IF v_usuario_id IS NOT NULL THEN
        DELETE FROM credenciales WHERE usuario_id = v_usuario_id;
        DELETE FROM relacion_aliado_tipo WHERE id_aliado = v_usuario_id;
        DELETE FROM relacion_necesidad_tipo WHERE id_necesidad IN (SELECT id FROM necesidades WHERE id_escuela = v_usuario_id);
        DELETE FROM necesidades WHERE id_escuela = v_usuario_id OR id_aliado = v_usuario_id;
        DELETE FROM usuarios WHERE id = v_usuario_id;
    END IF;
END;
$BODY$;

ALTER FUNCTION public.eliminar_usuario(character varying)
    OWNER TO postgres;
