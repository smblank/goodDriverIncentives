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

DROP FUNCTION IF EXISTS getUserID;

CREATE FUNCTION getUserID (userEmail VARCHAR(50))
RETURNS INT
READS SQL DATA
    BEGIN
        DECLARE id INT;

        SELECT userID INTO id
        FROM USER
        WHERE Email = userEmail;

        RETURN id;
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

DROP FUNCTION IF EXISTS createCatalog;

CREATE FUNCTION createCatalog ()
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        INSERT INTO ORG_CATALOG () VALUES ();

        SELECT CatalogID INTO newID
        FROM ORG_CATALOG
        WHERE CatalogID = @@Identity;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS createOrg;

CREATE FUNCTION createOrg (orgName VARCHAR(50), pointRate FLOAT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;
        DECLARE catalogue INT;

        SELECT createCatalog() INTO catalogue;

        INSERT INTO ORGANIZATION (Name, PointConversion, CatalogID) VALUES (orgName, pointRate, catalogue);

        SELECT OrgID INTO newID
        FROM ORGANIZATION
        WHERE OrgID = @@Identity;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS updateEmail;

CREATE FUNCTION updateEmail (oldEmail VARCHAR(50), newEmail VARCHAR(50))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE user INT;

        SELECT UserID INTO user
        FROM USER
        WHERE Email = oldEmail;

        UPDATE USER
            SET 
                Email = newEmail
        WHERE userID = user;

        RETURN user;
    END;;

DROP FUNCTION IF EXISTS updatePassword;

CREATE FUNCTION updatePassword (userEmail VARCHAR(50), newPass VARCHAR(20))
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE emailExists BOOLEAN;

        SELECT EXISTS (
            SELECT Email
            FROM USER
            WHERE Email = userEmail
        ) INTO emailExists;

        UPDATE USER
            SET HashedPassword = SHA(newPass)
        WHERE Email = userEmail;

        RETURN emailExists;
    END;;

DROP FUNCTION IF EXISTS addPassChange;

CREATE FUNCTION addPassChange (userEmail VARCHAR(50), changeType VARCHAR(10), currDate DATE)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newChange INT;
        DECLARE user INT;

        SELECT getUserID(userEmail) INTO user;
        
        INSERT INTO PASSWORD_CHANGE (ChangeDate, ChangeType, UserID) VALUES (currDate, changeType, user);

        SELECT ChangeNo INTO newChange
        FROM PASSWORD_CHANGE
        WHERE ChangeNo = @@Identity;

        RETURN newChange;
    END;;

DROP FUNCTION IF EXISTS addAddress;

CREATE FUNCTION addAddress (userEmail VARCHAR(50), newAddress VARCHAR(100))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newAddressId INT;
        DECLARE user INT;

        SELECT getUserID(userEmail) INTO user;
        
        INSERT INTO DRIVER_ADDRESSES (UserID, Address) VALUES (user, newAddress);

        SELECT AddressID INTO newAddressId
        FROM DRIVER_ADDRESSES
        WHERE AddressID = @@Identity;

        RETURN newAddressId;
    END;;
    
DROP FUNCTION IF EXISTS updateAddress;

CREATE FUNCTION updateAddress (userEmail VARCHAR(50), newAddress VARCHAR(100), oldAddress VARCHAR(100))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE user INT;
        DECLARE addressNo INT;

        SELECT getUserID(userEmail) INTO user;

        SELECT AddressId INTO addressNo
        FROM DRIVER_ADDRESSES
        WHERE Address = oldAddress;

        UPDATE DRIVER_ADDRESSES
            SET
                Address = newAddress
            WHERE AddressID = addressNo;
        
        RETURN 0;
    END;;

DELIMITER ;