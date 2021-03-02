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

/*Create driver address*/
CREATE FUNCTION createDriver (userName VARCHAR(100), userEmail VARCHAR(50), userPassword VARCHAR(20), addr VARCHAR(100), phone CHAR(12), organization INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        SELECT createUser(userName, userEmail, userPassword) INTO newID;

        IF newID > -1 THEN
            INSERT INTO DRIVER (UserID, PhoneNo, Points, OrgID) VALUES (newID, phone, 0, organization);
        END IF;

        RETURN newID;
    END;;

DROP FUNCTION IF EXISTS createApplicant;

CREATE FUNCTION createApplicant (currDate DATE, userName VARCHAR(100), email VARCHAR(50), phone CHAR(12), address VARCHAR(100), orgID INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newApplicant INT;

        INSERT INTO APPLICANT (ApplicantDate, IsAccepted, Reason, ApplicantName, Email, PhoneNo, HomeAddress, OrgID) VALUES (currDate, false, "Just applied", userName, email, phone, address, orgID);

        SELECT ApplicantID INTO newApplicant
        FROM APPLICANT
        WHERE ApplicantID = @@Identity;

        RETURN newApplicant;
    END;;

DROP FUNCTION IF EXISTS acceptApplicant;

CREATE FUNCTION acceptApplicant (userEmail VARCHAR(50), reasoning VARCHAR(150), randomPassword VARCHAR(20))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE driverName VARCHAR(100);
        DECLARE phone CHAR(12);
        DECLARE address VARCHAR(100);
        DECLARE org INT;
        DECLARE newDriver INT;

        UPDATE APPLICANT
            SET
                IsAccepted = true,
                Reason = reasoning
            WHERE Email = userEmail;

        SELECT ApplicantName, PhoneNo, HomeAddress, OrgID
        INTO driverName, phone, address, org
        FROM APPLICANT
        WHERE Email = userEmail;

        SELECT CreateDriver(driverName, userEmail, randomPassword, address, phone, org) INTO newDriver;

        RETURN newDriver;
    END;;

DROP FUNCTION IF EXISTS rejectApplicant;

CREATE FUNCTION rejectApplicant (userEmail VARCHAR(50), reasoning VARCHAR(150))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        UPDATE APPLICANT
            SET
                Reason = reasoning
            WHERE Email = userEmail;

        RETURN 0;
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

DROP FUNCTION IF EXISTS getUserName;

CREATE FUNCTION getUserName (userEmail VARCHAR(50))
RETURNS VARCHAR(100)
READS SQL DATA
    BEGIN
        DECLARE userName VARCHAR(100);

        SELECT Name INTO userName
        FROM USER
        WHERE Email = userEmail;

        RETURN userName;
    END;;

DROP FUNCTION IF EXISTS getDriverAddress;

CREATE FUNCTION getDriverAddress (userEmail VARCHAR(50))
RETURNS VARCHAR(100)
READS SQL DATA
    BEGIN
        DECLARE address VARCHAR(100);
        DECLARE user INT;

        SELECT getUserID(userEmail) INTO user;

        SELECT Address INTO address
        FROM DRIVER_ADDRESSES
        WHERE UserID = user;

        RETURN address;
    END;;

DROP FUNCTION IF EXISTS getDriverPhone;

CREATE FUNCTION getDriverPhone (userEmail VARCHAR(50))
RETURNS CHAR(12)
READS SQL DATA
    BEGIN
        DECLARE phone CHAR(12);
        DECLARE user INT;

        SELECT getUserID(userEmail) INTO user;

        SELECT PhoneNo INTO phone
        FROM DRIVER
        WHERE UserID = user;

        RETURN phone;
    END;;

DELIMITER ;