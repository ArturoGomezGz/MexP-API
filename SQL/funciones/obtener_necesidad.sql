-- FUNCTION: public.obtener_necesidad(integer)

-- DROP FUNCTION IF EXISTS public.obtener_necesidad(integer);

CREATE OR REPLACE FUNCTION public.obtener_necesidad(
	p_id_necesidad integer)
    RETURNS TABLE(id integer, nombre character varying, descripcion text, id_escuela integer, id_aliado integer) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT necesidades.id, necesidades.nombre, necesidades.descripcion, necesidades.id_escuela, necesidades.id_aliado
    FROM necesidades
    WHERE necesidades.id = p_id_necesidad;
END;
$BODY$;

ALTER FUNCTION public.obtener_necesidad(integer)
    OWNER TO postgres;
