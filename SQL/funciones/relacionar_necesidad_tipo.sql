-- FUNCTION: public.relacionar_necesidad_tipo(integer, integer)

-- DROP FUNCTION IF EXISTS public.relacionar_necesidad_tipo(integer, integer);

CREATE OR REPLACE FUNCTION public.relacionar_necesidad_tipo(
	p_id_necesidad integer,
	p_id_tipo_necesidad integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_id_relacion INT;
BEGIN
    -- Insertar la relación y obtener el ID generado
    INSERT INTO relacion_necesidad_tipo(id_tipo_necesidad, id_necesidad)
    VALUES (p_id_tipo_necesidad, p_id_necesidad)
    RETURNING id_relacion INTO v_id_relacion;

    -- Devolver el ID de la relación creada
    RETURN v_id_relacion;
END;
$BODY$;

ALTER FUNCTION public.relacionar_necesidad_tipo(integer, integer)
    OWNER TO postgres;
