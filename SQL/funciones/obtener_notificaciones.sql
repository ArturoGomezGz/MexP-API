-- FUNCTION: public.obtener_notificaciones(text, boolean)

-- DROP FUNCTION IF EXISTS public.obtener_notificaciones(text, boolean);

CREATE OR REPLACE FUNCTION public.obtener_notificaciones(
	p_usuario text,
	todos boolean)
    RETURNS TABLE(id integer, usuario_id integer, mensaje text, fecha timestamp without time zone, leido boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_usuario_id integer;
BEGIN
    -- Obtener el usuario_id a partir de p_usuario
    SELECT public.obtener_id_usuario(p_usuario) INTO v_usuario_id;

    RETURN QUERY 
    SELECT notificaciones.id, 
           notificaciones.usuario_id, 
           notificaciones.mensaje, 
           notificaciones.fecha, 
           notificaciones.leido
    FROM public.notificaciones
    WHERE notificaciones.usuario_id = v_usuario_id
    AND (todos OR notificaciones.leido = FALSE);
END;
$BODY$;

ALTER FUNCTION public.obtener_notificaciones(text, boolean)
    OWNER TO postgres;
