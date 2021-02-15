DELIMITER ;;

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
    END;;

DROP FUNCTION IF EXISTS createWishlist;

CREATE FUNCTION createWishlist (user INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        INSERT INTO WISHLIST (UserID) VALUES (user);

        SELECT ListID INTO newID
        FROM WISHLIST
        WHERE userID = user;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS createUser;

CREATE FUNCTION createUser (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE validEmail BOOLEAN;
        DECLARE newID INT;
        DECLARE wishID INT;
        /*Check unique email*/
        SELECT emailExists (userEmail) INTO validEmail FROM USER;

        IF validEmail = TRUE THEN
            SET newID = -1;
        ELSE
            INSERT INTO USER (Name, Email, HashedPassword) VALUES (userName, userEmail, SHA(userPassword));

            SELECT userID INTO newID
            FROM USER
            WHERE Email = userEmail;

            SELECT createWishlist(newID) INTO wishID;
        END IF;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS updateUser;

CREATE FUNCTION updateUser (user INT, userName VARCHAR(100), userEmail VARCHAR(50))
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE userExists BOOLEAN;

        SELECT EXISTS (
            SELECT userID
            FROM USER
        ) INTO userExists;

        UPDATE USER
            SET 
                Name = userName,
                Email = userEmail
        WHERE userID = user;

        RETURN userExists;
    END;;

DROP FUNCTION IF EXISTS createAdmin;

CREATE FUNCTION createAdmin (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        SELECT createUser(userName, userEmail, userPassword) INTO newID;

        IF newID > -1 THEN
            INSERT INTO ADMINISTRATOR (UserID) VALUES (newID);
        END IF;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS createSponsor;

CREATE FUNCTION createSponsor (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20), ccNum INT, ccSec INT, ccDate DATE, billAddress VARCHAR(100), organization INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        SELECT createUser(userName, userEmail, userPassword) INTO newID;

        IF newID > -1 THEN
            INSERT INTO SPONSOR (UserID, CreditCardNum, CreditCardSec, CreditCardDate, BillingAddress, OrgID) VALUES (newID, ccNum, ccSec, ccDate, billAddress, organization);
        END IF;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS createDriver;

CREATE FUNCTION createDriver (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20), addr VARCHAR(100), phone CHAR(12), organization INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        SELECT createUser(userName, userEmail, userPassword) INTO newID;

        IF newID > -1 THEN
            INSERT INTO DRIVER (UserID, Address, PhoneNo, Points, OrgID) VALUES (newID, addr, phone, 0, organization);
        END IF;

        RETURN newID;
    END;;

DELIMITER ;