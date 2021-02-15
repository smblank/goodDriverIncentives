DELIMITER $$

DROP FUNCTION IF EXISTS emailExists;

CREATE FUNCTION emailExists(userEmail VARCHAR(50))
RETURNS BOOLEAN
READS SQL DATA
    BEGIN
        DECLARE doesExist BOOLEAN;
        SELECT EXISTS (
            SELECT Email 
            FROM USER
            WHERE Email = userEmail) INTO doesExist;

        RETURN doesExist;
    END$$

DROP FUNCTION IF EXISTS createEntry;

CREATE FUNCTION createEntry (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20))
RETURNS INT
    BEGIN
        DECLARE validEmail BOOLEAN;
        DECLARE errorCode INT;
        /*Check unique email*/
        SELECT emailExists (userEmail) INTO validEmail FROM USER;

        IF validEmail = FALSE THEN
            SET errorCode = -1;
        ELSE
            INSERT INTO USER (Name, Email, HashedPassword) VALUES (userName, userEmail, SHA(userPassword));
            SET errorCode = 0;
        END IF;

        RETURN errorCode;
    END$$

DELIMITER ;