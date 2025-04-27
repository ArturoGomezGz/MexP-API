CREATE OR REPLACE FUNCTION public.obtener_usuario_por_id(
    p_id integer
)
RETURNS TABLE(id integer, nombre character varying, correo character varying, direccion text, tipo_usuario character varying) 
LANGUAGE 'plpgsql'
COST 100
VOLATILE PARALLEL UNSAFE
ROWS 1000
AS $BODY$
BEGIN

    RETURN QUERY
    SELECT u.id, u.nombre, u.correo, u.direccion, tu.nombre AS tipo_usuario
    FROM usuarios u
    JOIN tipo_usuarios tu ON u.tipo_usuario_id = tu.id
    WHERE u.id = p_id;
END;
$BODY$;

ALTER FUNCTION public.obtener_usuario_por_id(integer)
    OWNER TO postgres;