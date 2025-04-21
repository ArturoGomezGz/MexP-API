-- FUNCTION: public.obtener_usuario(character varying)

-- DROP FUNCTION IF EXISTS public.obtener_usuario(character varying);

CREATE OR REPLACE FUNCTION public.obtener_usuario(
	p_correo character varying)
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
    WHERE u.correo = p_correo;
END;
$BODY$;

ALTER FUNCTION public.obtener_usuario(character varying)
    OWNER TO postgres;
