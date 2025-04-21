-- FUNCTION: public.obtener_r_aliado_escuela(text)

-- DROP FUNCTION IF EXISTS public.obtener_r_aliado_escuela(text);

CREATE OR REPLACE FUNCTION public.obtener_r_aliado_escuela(
	p_correo_aliado text)
    RETURNS TABLE(id_aliado integer, aliado character varying, id_necesidad integer, necesidad character varying, id_escuela integer, escuela character varying, prioridad bigint) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
    v_id_aliado INT;
BEGIN
    -- Obtener el ID de la escuela a partir del correo
    v_id_aliado := public.obtener_id_usuario(p_correo_aliado);

    -- Retornar los registros filtrados por la escuela y la necesidad
    RETURN QUERY 
    SELECT * 
    FROM vr_aliado_escuela AS v
    WHERE v.id_aliado = v_id_aliado
	ORDER BY v.prioridad DESC;
	
END;
$BODY$;

ALTER FUNCTION public.obtener_r_aliado_escuela(text)
    OWNER TO postgres;
