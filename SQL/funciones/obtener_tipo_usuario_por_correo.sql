-- FUNCTION: public.obtener_tipo_usuario_por_correo(text)

-- DROP FUNCTION IF EXISTS public.obtener_tipo_usuario_por_correo(text);

CREATE OR REPLACE FUNCTION public.obtener_tipo_usuario_por_correo(
	p_correo text)
    RETURNS text
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_tipo_usuario TEXT;
BEGIN
    -- Obtener el tipo de usuario basado en el correo
    SELECT tipo_usuario_id INTO v_tipo_usuario 
    FROM usuarios 
    WHERE correo = p_correo;

    -- Retornar el tipo de usuario
    RETURN v_tipo_usuario;
END 
$BODY$;

ALTER FUNCTION public.obtener_tipo_usuario_por_correo(text)
    OWNER TO postgres;
