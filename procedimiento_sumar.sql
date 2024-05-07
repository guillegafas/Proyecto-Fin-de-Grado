
ALTER TABLE pedidos
ADD COLUMN puntos_sumados BOOLEAN DEFAULT FALSE;


DELIMITER //
CREATE PROCEDURE SUMAR_PUNTOS ()
	BEGIN
	DECLARE CLIENTE_ID INT;
    DECLARE PEDIDOS_PUNTOS INT;
    DECLARE DONE INT DEFAULT FALSE;
    DECLARE CUR1 CURSOR FOR SELECT id_cliente, puntos_pedido from pedidos where puntos_sumados = FALSE;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET DONE = TRUE;
		OPEN CUR1;
			BUCLE:LOOP
				FETCH CUR1 INTO cliente_id, PEDIDOS_PUNTOS;
					IF DONE THEN LEAVE BUCLE;
					ELSE
						   UPDATE clientes SET puntos = puntos + pedidos_puntos WHERE id_cliente = cliente_id;
                           UPDATE pedidos SET puntos_sumados = TRUE WHERE id_cliente = cliente_id AND pedidos_puntos = puntos_pedido;
					END IF;
			END LOOP;
		CLOSE CUR1;
END // 
DELIMITER ; 


DELIMITER //

CREATE TRIGGER actualizar_puntos
BEFORE INSERT ON pedidos
FOR EACH ROW
BEGIN
    -- Actualizar los puntos del cliente en la tabla clientes
    UPDATE clientes
    SET puntos = puntos + NEW.puntos_pedido
    WHERE id_cliente = NEW.id_cliente;

    -- Marcar los puntos como sumados en el nuevo registro de pedidos
    SET NEW.puntos_sumados = TRUE;
END;
//
DELIMITER ;

DELIMITER //

CREATE EVENT actualizar_puntos_cada_15_minutos
ON SCHEDULE EVERY 15 MINUTE
DO
BEGIN
    CALL actualizar_puntos_despues_de_pedido();
END//

DELIMITER ;


SELECT * FROM INFORMATION_SCHEMA.EVENTS;