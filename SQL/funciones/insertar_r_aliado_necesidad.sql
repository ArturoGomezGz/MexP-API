-- FUNCTION: public.insertar_r_aliado_necesidad(text, integer)

-- DROP FUNCTION IF EXISTS public.insertar_r_aliado_necesidad(text, integer);

CREATE OR REPLACE FUNCTION public.insertar_r_aliado_necesidad(
	p_aliado text,
	p_id_necesidad integer)
    RETURNS boolean
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_id_aliado INTEGER;
BEGIN
    SELECT obtener_id_usuario(p_aliado) INTO v_id_aliado;

    INSERT INTO relacion_aliado_necesidad (id_aliado, id_necesidad) VALUES (v_id_aliado, p_id_necesidad);

    RETURN TRUE;
END;
$BODY$;

ALTER FUNCTION public.insertar_r_aliado_necesidad(text, integer)
    OWNER TO postgres;
