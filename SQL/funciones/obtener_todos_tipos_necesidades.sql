-- FUNCTION: public.obtener_todos_tipos_necesidades()

-- DROP FUNCTION IF EXISTS public.obtener_todos_tipos_necesidades();

CREATE OR REPLACE FUNCTION public.obtener_todos_tipos_necesidades(
	)
    RETURNS TABLE(id integer, nombre character varying, descripcion text) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY SELECT tipo_necesidad.id, tipo_necesidad.nombre, tipo_necesidad.descripcion FROM tipo_necesidad;
END;
$BODY$;

ALTER FUNCTION public.obtener_todos_tipos_necesidades()
    OWNER TO postgres;
