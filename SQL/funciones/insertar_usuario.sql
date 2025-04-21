    -- FUNCTION: public.insertar_usuario(character varying, character varying, character varying, text, integer, text)

-- DROP FUNCTION IF EXISTS public.insertar_usuario(character varying, character varying, character varying, text, integer, text);

CREATE OR REPLACE FUNCTION public.insertar_usuario(
	p_nombre character varying,
	p_correo character varying,
	p_numero character varying,
	p_direccion text,
	p_tipo_usuario_id integer,
	p_password_hash text)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    v_usuario_id INT;
BEGIN
    -- Insertar el usuario en la tabla usuarios
    INSERT INTO usuarios (nombre, correo, numero, direccion, tipo_usuario_id)
    VALUES (p_nombre, p_correo, p_numero, p_direccion, p_tipo_usuario_id)
    RETURNING id INTO v_usuario_id;

    -- Insertar la contraseña en la tabla credenciales
    INSERT INTO credenciales (usuario_id, password_hash)
    VALUES (v_usuario_id, p_password_hash);
END;
$BODY$;

ALTER FUNCTION public.insertar_usuario(character varying, character varying, character varying, text, integer, text)
    OWNER TO postgres;
