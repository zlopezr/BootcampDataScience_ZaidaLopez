### Conexión a la base de datos 
USE sakila;
### Parte 1 – SELECT y WHERE
	##  1. Mostrar nombre y apellido de todos los clientes
	SELECT first_name,last_name FROM customer;
    
	##  2. Películas con duración mayor a 120 minutos
	SELECT title,length FROM film
	WHERE length > 120;
    
## Parte 2 – ORDER BY
	#3. Ordenar clientes por apellido --> Por orden alfabetico de la A a la Z
	SELECT first_name, last_name FROM customer
	ORDER BY last_name ASC;
    
	#4. Top 5 películas más largas --> TIP: Use la palabra LIMIT
	SELECT title, length  FROM film
	ORDER BY length DESC
	LIMIT 5;
    
## Parte 3 – INNER JOIN
	# 5. Cantidad pagada y fecha del pago con nombre y apellido del cliente (JOIN entre Payment - Customer)
    SELECT first_name, last_name, p.amount, p.payment_date FROM payment p
    JOIN customer c ON p.customer_id = c.customer_id;
    
	# 6. Películas alquiladas (JOIN entre Rental - Inventory - Film)
	SELECT title,description,release_year,rental_duration,rental_rate,length,replacement_cost,rating,special_features,rental_date,return_date FROM rental r
    JOIN inventory i on r.inventory_id = i.inventory_id
    JOIN film f on i.film_id= f.film_id;
    
## Parte 4 – LEFT JOIN
	#7. Nombre y apellido de clientes sin pagos (LEFT JOIN entre Payment - Customer pero usando WHERE)
    SELECT  first_name,last_name FROM customer c
    LEFT JOIN Payment p on c.customer_id= p.customer_id
    WHERE p.amount = 0;
    
	#8. Listar los nombres de las peliculas y su duracion de aquellos titulos que no tienen actores 
	SELECT f.title, f.length FROM film f
	LEFT JOIN film_actor f_a ON f.film_id = f_a.film_id
	WHERE f_a.actor_id IS NULL;
    
## Parte 5 – INSERT, UPDATE, DELETE (Data Definition Language ) **RECUERDA USAR WHERE**
	#9. Insertar actor temporal
	INSERT INTO actor (first_name, last_name)
	VALUES ('ZAIDA','LOPEZ');
    
	#10. Actualizar actor
    UPDATE actor
	SET 
	first_name = 'MARIA',
	last_name = 'ROMERO'
	WHERE actor_id = 202;

	#11. Eliminar actor
    DELETE FROM actor
    WHERE actor_id = 202;

## Parte 6 - Consultas Avanzadas
	#12. Top 5 clientes con mayor cantidad de dinero pagado al servicio de rentas
	SELECT c.customer_id, c.first_name, c.last_name, SUM(p.amount) AS total_pagado 	FROM customer c
	JOIN payment p ON c.customer_id = p.customer_id
	GROUP BY c.customer_id, c.first_name, c.last_name
	ORDER BY total_pagado DESC
	LIMIT 5;
    
	#13. Top 5 Películas más alquiladas  (JOIN entre Rental - Inventory - Film) --> Agrupar los datos con conteo y tomar las mejores 5 
	SELECT title, count(*) AS total_ventas FROM rental A
    LEFT JOIN inventory I ON A.inventory_id = I.inventory_id
    LEFT JOIN film F ON I.film_id = F.film_id
    GROUP BY F.title
    ORDER BY total_ventas DESC
    Limit 5;