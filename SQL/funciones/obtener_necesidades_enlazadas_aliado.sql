-- FUNCTION: public.obtener_necesidades_enlazadas_aliado(text)

-- DROP FUNCTION IF EXISTS public.obtener_necesidades_enlazadas_aliado(text);

CREATE OR REPLACE FUNCTION public.obtener_necesidades_enlazadas_aliado(
	p_correo text)
    RETURNS TABLE(id integer, nombre character varying, descripcion text, id_escuela integer, id_aliado integer, completada boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_id_aliado INTEGER;
BEGIN
    -- Obtener el ID del aliado basado en su correo
    SELECT obtener_id_usuario(p_correo) INTO v_id_aliado;

    -- Ejecutar la consulta solo si encontramos un aliado
    IF v_id_aliado IS NOT NULL THEN
        RETURN QUERY
        SELECT n.id, n.nombre, n.descripcion, n.id_escuela, n.id_aliado, n.completada
        FROM necesidades AS n
        WHERE n.id_aliado = v_id_aliado;
    END IF;
END;
$BODY$;

ALTER FUNCTION public.obtener_necesidades_enlazadas_aliado(text)
    OWNER TO postgres;
