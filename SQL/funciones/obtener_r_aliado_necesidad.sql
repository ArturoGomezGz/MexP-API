-- FUNCTION: public.obtener_r_aliado_necesidad(text, integer)

-- DROP FUNCTION IF EXISTS public.obtener_r_aliado_necesidad(text, integer);

CREATE OR REPLACE FUNCTION public.obtener_r_aliado_necesidad(
	p_correo_aliado text,
	p_id_necesidad integer)
    RETURNS TABLE(id integer, id_aliado integer, id_necesidad integer, fecha_creacion timestamp without time zone) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_id_aliado INTEGER;
BEGIN
    -- Obtener el ID del aliado usando su correo
    SELECT obtener_id_usuario(p_correo_aliado) INTO v_id_aliado;

    -- Validar que el usuario existe
    IF v_id_aliado IS NULL THEN
        RETURN;
    END IF;

    -- Retornar la relación filtrada por el ID del aliado y la necesidad
    RETURN QUERY
    SELECT id, id_aliado, id_necesidad, fecha_creacion
    FROM public.relacion_aliado_necesidad
    WHERE id_aliado = v_id_aliado AND id_necesidad = p_id_necesidad;
END;
$BODY$;

ALTER FUNCTION public.obtener_r_aliado_necesidad(text, integer)
    OWNER TO postgres;
