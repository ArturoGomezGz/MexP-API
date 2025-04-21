-- FUNCTION: public.insertar_notificacion(text, text)

-- DROP FUNCTION IF EXISTS public.insertar_notificacion(text, text);

CREATE OR REPLACE FUNCTION public.insertar_notificacion(
	p_usuario text,
	p_mensaje text)
    RETURNS boolean
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_usuario_id integer;
BEGIN
    -- Obtener el usuario_id a partir de p_usuario
    SELECT public.obtener_id_usuario(p_usuario) INTO v_usuario_id;

    -- Insertar la notificación
    INSERT INTO public.notificaciones (usuario_id, mensaje)
    VALUES (v_usuario_id, p_mensaje);

    -- Retornar TRUE tras la inserción exitosa
    RETURN TRUE;
END;
$BODY$;

ALTER FUNCTION public.insertar_notificacion(text, text)
    OWNER TO postgres;
