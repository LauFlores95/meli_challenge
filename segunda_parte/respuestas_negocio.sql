-----------------
-- Ejercicio 1 --
-----------------

SELECT 
	S.id_seller AS id_seller,
	S.nombre AS nombre,
	S.apellido AS apellido,
	S.fecha_nacimiento AS fecha_nacimiento,
	SUM(O.cantidad_unidades) AS cantidad_ventas
FROM db.Order O 
LEFT JOIN db.Seller S ON O.id_seller = S.id_seller
WHERE 
	-- Esto lo hago asi porque tengo que asegurarme la igualdad en tipo de datos
	S.fecha_nacimiento = FORMAT(GETDATE(), 'yyyy-MM-dd') AND
	FORMAT(O.fecha_transaccion, 'yyyy-MM-dd') BETWEEN ('2020-01-01' AND '2020-01-31')
GROUP BY 
	S.id_seller, 
	S.nombre, 
	S.apellido, 
	S.fecha_nacimiento
HAVING SUM(O.cantidad_unidades) > 1500
;

-----------------
-- Ejercicio 2 --
-----------------

SELECT DISTINCT
	subquery.id_category AS id_category,
	subquery.nombre_vendedor AS nombre_vendedor,
	subquery.apellido_vendedor AS apellido_vendedor,
	subquery.año_transaccion AS año_transaccion,
	subquery.mes_transaccion AS mes_transaccion,
	subquery.cantidad_ventas AS cantidad_unidades,
	subquery.cantidad_ventas AS cantidad_transacciones,
	subquery.monto_total_transaccionado AS monto_total_transaccionado
FROM (
	SELECT DISTINCT
		C.id_category AS id_category,
		S.id_seller AS id_seller,
		S.nombre AS nombre_vendedor,
		S.apellido AS apellido_vendedor,
		YEAR(O.fecha_transaccion) AS año_transaccion,
		MONTH(O.fecha_transaccion) AS mes_transaccion,
		SUM(O.cantidad_unidades) AS cantidad_unidades,
		COUNT(O.id_order) AS cantidad_transacciones,
		SUM(O.monto_total) AS monto_total_transaccionado,
		-- Genero un ID particionado para despues poder filtrar el TOP 5 de interes.
		ROW_NUMBER() OVER 
			(PARTITIONED BY C.id_category, 
							S.id_seller, 
							YEAR(O.fecha_transaccion), 
							MONTH(O.fecha_transaccion) 
			ORDER BY COUNT(O.id_order) DESC) 
		AS rank
	FROM db.Order O
	LEFT JOIN (
		SELECT DISTINCT
			id_category
		FROM db.Category 
		WHERE 
			descripcion_categoria = 'Celulares'
		-- Esta subquery esta hecha para traer solo el ID 
		-- correspondiente a los celulares y 
		-- poder utilizar esta PK como parámetro de 
		-- Joineo ya que es de tipo INT. Luego de filtrar por este id, se "limpiarian"
		-- los posibles NULLS que resulten del JOIN
		) C ON O.id_category = C.id_category
	LEFT JOIN db.Seller S ON O.id_seller = S.id_seller
	WHERE 
		O.id_category = C.id_category AND -- Filtro por id de los celulares
		O.fecha_transaccion BETWEEN '2020-01-01' AND '2020-12-31'
	GROUP BY 
		C.id_category,
		S.id_seller,
		YEAR(O.fecha_transaccion),
		MONTH(O.fecha_transaccion)
	) subquery
WHERE rank < 5;

-----------------
-- Ejercicio 3 --
-----------------

CREATE PROCEDURE ingesta_item_status
AS 
BEGIN
	-- Declaro la variable que registrara la fecha de actualizacion que va a ser
	-- el ultimo dia cerrado (ayer)
	DECLARE @ultimo_dia DATE = CAST(DATEADD(DAY, -1, GETDATE()) AS DATE);

	-- Si el SP se ejecuta a fin del dia:
	--DECLARE @ultimo_dia DATE = CAST(GETDATE() AS DATE);

	-- Elimino los registros ya existentes en la tabla para que quede vacia
	DELETE FROM db.Item_status
	WHERE fecha = @ultimo_dia;

	-- INSERT de los datos de la ultima foto
	INSERT INTO db.Item_status (id_item, fecha, ultimo_precio_registrado, cantidad_vendida, estado) 
	SELECT 
		I.id_item AS id_item,
		@ultimo_dia AS fecha,
		I.ultimo_precio_registrado AS ultimo_precio_registrado,
		O.cantidad_vendida AS cantidad_vendida,
		I.estado AS estado
	FROM df.Item I 
	LEFT JOIN (
		-- Me traigo la fecha y la suma de todas las unidades que se vendieron el @ultimo_dia
		SELECT  
			fecha_transaccion AS fecha,
			SUM(cantidad_unidades) AS cantidad_vendida,
		FROM db.Order 
		WHERE fecha_transaccion = @ultimo_dia
		GROUP BY 
			fecha_transaccion
			) O ON I.fecha_transaccion = O.fecha
	WHERE I.fecha_transaccion = @ultimo_dia;


