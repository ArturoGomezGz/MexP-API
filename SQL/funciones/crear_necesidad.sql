-- FUNCTION: public.crear_necesidad(text, text, text)

-- DROP FUNCTION IF EXISTS public.crear_necesidad(text, text, text);

CREATE OR REPLACE FUNCTION public.crear_necesidad(
	p_correo text,
	p_nombre text,
	p_descripcion text)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_id_usuario INT;
    v_tipo_usuario INT;
    v_id_escuela INT;
    v_id_necesidad INT;
BEGIN
    -- Obtener ID de usuario y tipo de usuario
    SELECT obtener_id_usuario(p_correo) INTO v_id_usuario;
    SELECT obtener_tipo_usuario_por_correo(p_correo) INTO v_tipo_usuario;
    
    -- Asignar ID de escuela igual al ID de usuario
    v_id_escuela := v_id_usuario;

    -- Verificar que el usuario es tipo 2
    IF v_tipo_usuario = 2 THEN
        -- Insertar la necesidad y obtener el ID generado
        INSERT INTO necesidades(nombre, descripcion, id_escuela)
        VALUES (p_nombre, p_descripcion, v_id_escuela)
        RETURNING id INTO v_id_necesidad;

        -- Devolver el ID de la necesidad generada
        RETURN v_id_necesidad;
    ELSE
        -- Lanzar un error si el usuario no tiene permisos
        RAISE EXCEPTION 'El usuario no tiene permisos para esta acción';
    END IF;
END;
$BODY$;

ALTER FUNCTION public.crear_necesidad(text, text, text)
    OWNER TO postgres;
