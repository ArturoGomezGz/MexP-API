-- FUNCTION: public.relacionar_aliado_tipo(character varying, integer)

-- DROP FUNCTION IF EXISTS public.relacionar_aliado_tipo(character varying, integer);

CREATE OR REPLACE FUNCTION public.relacionar_aliado_tipo(
	correo_aliado character varying,
	id_tipo_necesidad integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    id_aliado INTEGER;
    tipo_usuario INTEGER;
    nuevo_id_relacion INTEGER;
BEGIN
    -- Obtener el ID del aliado a partir del correo
    SELECT obtener_id_usuario(correo_aliado) INTO id_aliado;

    -- Si el usuario no existe, salir sin hacer nada
    IF id_aliado IS NULL THEN
        RETURN NULL;
    END IF;

    -- Obtener el tipo de usuario a partir del correo
    SELECT obtener_tipo_usuario_por_correo(correo_aliado) INTO tipo_usuario;

    -- Si el tipo de usuario no es 3, salir sin hacer nada
    IF tipo_usuario <> 3 THEN
        RETURN NULL;
    END IF;

    -- Insertar la relación en la tabla y obtener el nuevo ID
    INSERT INTO relacion_aliado_tipo(id_tipo_necesidad, id_aliado)
    VALUES (id_tipo_necesidad, id_aliado)
    RETURNING id_relacion INTO nuevo_id_relacion;

    -- Devolver el ID recién insertado
    RETURN nuevo_id_relacion;
END;
$BODY$;

ALTER FUNCTION public.relacionar_aliado_tipo(character varying, integer)
    OWNER TO postgres;
