-- FUNCTION: public.actualizar_estado_notificacion(text, integer, boolean)

-- DROP FUNCTION IF EXISTS public.actualizar_estado_notificacion(text, integer, boolean);

CREATE OR REPLACE FUNCTION public.actualizar_estado_notificacion(
	p_usuario text,
	p_notificacion_id integer,
	p_leido boolean)
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

    -- Verificar que la notificación pertenece al usuario
    IF NOT EXISTS (
        SELECT 1 FROM public.notificaciones 
        WHERE id = p_notificacion_id 
        AND usuario_id = v_usuario_id
    ) THEN
        RETURN FALSE; -- La notificación no pertenece al usuario
    END IF;

    -- Actualizar la notificación con el nuevo valor de leido
    UPDATE public.notificaciones
    SET leido = p_leido
    WHERE id = p_notificacion_id;

    RETURN TRUE; -- Retornar TRUE si la actualización fue exitosa
END;
$BODY$;

ALTER FUNCTION public.actualizar_estado_notificacion(text, integer, boolean)
    OWNER TO postgres;
