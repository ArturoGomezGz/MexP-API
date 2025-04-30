-- FUNCTION: public.obtener_r_escuela_aliado(text, integer)

-- DROP FUNCTION IF EXISTS public.obtener_r_escuela_aliado(text, integer);

CREATE OR REPLACE FUNCTION public.obtener_r_escuela_aliado(
	p_correo_escuela text,
	p_id_necesidad integer)
    RETURNS TABLE(id_escuela integer, escuela character varying, id_necesidad integer, necesidad character varying, aliado character varying, id_aliado integer, prioridad bigint, correo_aliado character varying) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_id_escuela INT;
BEGIN
    -- Obtener el ID de la escuela a partir del correo
    v_id_escuela := public.obtener_id_usuario(p_correo_escuela);

    -- Retornar los registros filtrados por la escuela y la necesidad
    RETURN QUERY 
    SELECT v.id_escuela, v.escuela, v.id_necesidad, v.necesidad, v.aliado, v.id_aliado, v.prioridad, v.correo_aliado
    FROM vr_escuela_aliado AS v
	JOIN necesidades AS n ON n.id = v.id_necesidad
    WHERE v.id_escuela = v_id_escuela 
    AND (p_id_necesidad = 0 OR v.id_necesidad = p_id_necesidad)
	AND n.id_aliado IS NULL
    ORDER BY v.prioridad DESC;
END;
$BODY$;

ALTER FUNCTION public.obtener_r_escuela_aliado(text, integer)
    OWNER TO postgres;
