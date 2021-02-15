DELIMITER ;;

DROP FUNCTION IF EXISTS isInCatalog;

CREATE FUNCTION isInCatalog (product INT, catalogue INT)
RETURNS BOOLEAN
READS SQL DATA
    BEGIN
        DECLARE inCatalog BOOLEAN;

        SELECT EXISTS (
            SELECT ProductID
            FROM IS_IN_CATALOG
            WHERE CatalogID = catalogue
        ) INTO inCatalog;

        RETURN inCatalog;
    END;;

DROP FUNCTION IF EXISTS addToCatalog;

CREATE FUNCTION addToCatalog (product INT, catalogue INT)
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE productExists BOOLEAN;

        SELECT EXISTS (
            SELECT ProductID
            FROM PRODUCT
            WHERE ProductID = product
        ) INTO productExists;

        IF productExists <> FALSE THEN
            INSERT INTO IS_IN_CATALOG (CatalogID, ProductID) VALUES (catalogue, product);
        END IF;

        RETURN productExists;
    END;;

DROP FUNCTION IF EXISTS removeFromCatalog;

CREATE FUNCTION removeFromCatalog (product INT, catalogue INT)
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE productExists BOOLEAN;
        DECLARE inCatalog BOOLEAN;

        SELECT EXISTS (
            SELECT ProductID
            FROM PRODUCT
            WHERE ProductID = product
        ) INTO productExists;

        IF productExists <> FALSE THEN
            SELECT isInCatalog(product, catalogue) INTO inCatalog;
            IF isInCatalog <> FALSE THEN
                DELETE FROM IS_IN_CATALOG WHERE catalogID = catalogue AND productID = product;
            END IF;
        END IF;

        RETURN productExists AND inCatalog;
    END;;

DROP FUNCTION IF EXISTS createOrder;

CREATE FUNCTION createOrder (driver INT, dateCreated DATE)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newID INT;

        INSERT INTO DRIVER_ORDER (OrderDate) VALUES (dateCreated);

        SELECT OrderID INTO newID
        FROM DRIVER_ORDER
        WHERE OrderID = @@Identity;

        INSERT INTO BELONGS_TO (UserID, OrderID) VALUES (driver, newID);

        RETURN newID;
    END;;

/*DROP FUNCTION IF EXISTS addToOrder;

CREATE FUNCTION addToOrder (order INT, product INT, qty INT)*/

DELIMITER ;