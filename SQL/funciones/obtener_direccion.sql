CREATE OR REPLACE FUNCTION public.obtener_direccion(
    p_id integer
) RETURNS TABLE (
    id integer,
    direccion text,
    latitud text,
    longitud text
) LANGUAGE 'plpgsql'
COST 100
VOLATILE PARALLEL UNSAFE
ROWS 1000
AS $BODY$
BEGIN
    RETURN QUERY
    SELECT u.id, u.direccion, u.latitud, u.longitud
    FROM usuarios u
    WHERE u.id = p_id;
END;
$BODY$;

ALTER FUNCTION public.obtener_direccion(integer)
    OWNER TO postgres;