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

DROP FUNCTION IF EXISTS addToOrder;

CREATE FUNCTION addToOrder (orderID INT, product INT, qty INT)
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE productExists BOOLEAN;

        SELECT EXISTS (
            SELECT ProductID
            FROM Product
            WHERE ProductID = product
        ) INTO productExists;

        IF productExists = TRUE THEN
            INSERT INTO IS_IN_ORDER (OrderID, ProductID, Quantity) VALUES (orderID, product, qty);
        END IF;

        RETURN productExists;
    END;;

DROP FUNCTION IF EXISTS removeFromOrder;

CREATE FUNCTION removeFromOrder (orderID INT, product INT)
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE orderExists BOOLEAN;

        SELECT EXISTS (
            SELECT OrderID
            FROM IS_IN_ORDER
            WHERE OrderID = orderID AND ProductID = product
        ) INTO orderExists;

        DELETE FROM IS_IN_ORDER WHERE OrderID = orderID AND ProductID = product;

        RETURN orderExists;
    END;;

DROP FUNCTION IF EXISTS updateQuantity;

CREATE FUNCTION updateQuantity (orderID INT, product INT, newQty INT)
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE orderExists BOOLEAN;

        SELECT EXISTS (
            SELECT OrderID, ProductID
            FROM IS_IN_ORDER
            WHERE OrderID = orderID AND ProuctID = product
        ) INTO orderExists;

        IF orderExists = TRUE THEN
            UPDATE IS_IN_ORDER
            SET
                Quantity = newQty
            WHERE OrderID = orderID AND ProductID = product;
        END IF;

        RETURN orderExists;
    END;;

DROP FUNCTION IF EXISTS isInOrder;

CREATE FUNCTION isInOrder (orderID INT, product INT)
RETURNS BOOLEAN
READS SQL DATA
    BEGIN
        DECLARE inOrder BOOLEAN;

        SELECT EXISTS (
            SELECT OrderID, ProductID
            FROM IS_IN_ORDER
            WHERE OrderID = orderID AND ProductID = product
        ) INTO inOrder;

        RETURN inOrder;
    END;;

DROP FUNCTION IF EXISTS addToWishlist;

CREATE FUNCTION addToWishlist (driver INT, product INT)
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE productExists BOOLEAN;
        DECLARE list INT;

        SELECT EXISTS (
            SELECT ProductID
            FROM PRODUCT
            WHERE ProductID = product
        ) INTO productExists;

        IF productExists = TRUE THEN
            SELECT ListID INTO list
            FROM WISHLIST
            WHERE UserID = driver;

            INSERT INTO IS_IN_WISHLIST (ProductID, ListID) VALUES (product, list);
        END IF;

        RETURN productExists;
    END;;

DROP FUNCTION IF EXISTS removeFromWishlist;

CREATE FUNCTION removeFromWishlist (driver INT, product INT)
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE productExists BOOLEAN;
        DECLARE list INT;

        SELECT EXISTS (
            SELECT ProductID
            FROM PRODUCT
            WHERE ProductID = product
        ) INTO productExists;

        IF productExists = TRUE THEN
            SELECT ListID INTO list
            FROM WISHLIST
            WHERE UserID = driver;

            DELETE FROM IS_IN_WISHLIST WHERE ListID = list AND ProductID = product;
        END IF;

        RETURN productExists;
    END;;

DROP FUNCTION IF EXISTS isInWishlist;

CREATE FUNCTION isInWishlist (driver INT, product INT)
RETURNS BOOLEAN
READS SQL DATA
    BEGIN
        DECLARE inWishlist BOOLEAN;
        DECLARE list INT;

        SELECT ListID INTO list
        FROM WISHLIST
        WHERE UserID = driver;

        SELECT EXISTS(
            SELECT ListID, ProductID
            FROM IS_IN_WISHLIST
            WHERE ListID = list AND ProductID = product
        ) INTO inWishlist;

        RETURN inWishlist;
    END;;

DELIMITER ;