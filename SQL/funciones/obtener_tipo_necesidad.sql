-- FUNCTION: public.obtener_tipo_necesidad(integer)

-- DROP FUNCTION IF EXISTS public.obtener_tipo_necesidad(integer);

CREATE OR REPLACE FUNCTION public.obtener_tipo_necesidad(
	p_id_tipo_necesidad integer)
    RETURNS TABLE(id integer, nombre character varying, descripcion text) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT tipo_necesidad.id, tipo_necesidad.nombre, tipo_necesidad.descripcion
    FROM tipo_necesidad
    WHERE tipo_necesidad.id = p_id_tipo_necesidad;
END;
$BODY$;

ALTER FUNCTION public.obtener_tipo_necesidad(integer)
    OWNER TO postgres;
