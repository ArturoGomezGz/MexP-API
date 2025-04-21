-- FUNCTION: public.vincular_necesidad_aliado(text, integer, text)

-- DROP FUNCTION IF EXISTS public.vincular_necesidad_aliado(text, integer, text);

CREATE OR REPLACE FUNCTION public.vincular_necesidad_aliado(
	p_escuela text,
	p_necesidad integer,
	p_aliado text)
    RETURNS boolean
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_escuela_id integer;
    v_aliado_id integer;
BEGIN
    -- Obtener el id de la escuela usando la función pública
    SELECT public.obtener_id_usuario(p_escuela) INTO v_escuela_id;
    
    -- Si la escuela no existe, retornar FALSE
    IF v_escuela_id IS NULL THEN
        RETURN FALSE;
    END IF;

    -- Obtener el id del aliado usando la función pública
    SELECT public.obtener_id_usuario(p_aliado) INTO v_aliado_id;

    -- Si el aliado no existe, retornar FALSE
    IF v_aliado_id IS NULL THEN
        RETURN FALSE;
    END IF;

    -- Verificar que la necesidad pertenece a la escuela
    IF NOT EXISTS (
        SELECT 1 FROM public.necesidades 
        WHERE id = p_necesidad AND id_escuela = v_escuela_id
    ) THEN
        RETURN FALSE; -- La necesidad no pertenece a la escuela
    END IF;

    -- Actualizar la necesidad con el nuevo aliado
    UPDATE public.necesidades
    SET id_aliado = v_aliado_id
    WHERE id = p_necesidad;

    -- Retornar TRUE si la actualización fue exitosa
    RETURN TRUE;
END;
$BODY$;

ALTER FUNCTION public.vincular_necesidad_aliado(text, integer, text)
    OWNER TO postgres;
