/*HASHBYTES('SHA2_512', userPass)*/

DELIMITER $$

CREATE FUNCTION emailExists(userEmail VARCHAR(50))
RETURNS BOOLEAN
READS SQL DATA
    BEGIN
        DECLARE doesExist BOOLEAN;
        SELECT EXISTS (
            SELECT EMAIL 
            FROM USER
            WHERE Email = userEmail) INTO doesExist;

        RETURN doesExist;
    END$$

DELIMITER ;