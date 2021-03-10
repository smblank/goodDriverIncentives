DELIMITER ;;

DROP FUNCTION IF EXISTS createProduct;

CREATE FUNCTION createProduct (name VARCHAR(45), price FLOAT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newProduct INT;

        INSERT INTO PRODUCT (ProductName, Price)
        VALUES (name, price);

        SELECT ProductId INTO newProduct
        FROM PRODUCT
        WHERE ProductID = @@Identity;

        RETURN newProduct;
    END;;

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

DROP FUNCTION IF EXISTS cancelOrder;

CREATE FUNCTION cancelOrder (orderID INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DELETE FROM DRIVER_ORDER
        WHERE OrderID = orderID;

        RETURN 0;
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

DROP FUNCTION IF EXISTS updatePrice;

CREATE FUNCTION updatePrice(product INT, newPrice FLOAT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        UPDATE PRODUCT
            SET
                Price = newPrice
            WHERE ProductID = product;
        
        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS updateAvailability;

CREATE FUNCTION updateAvailability (product INT, newAvailability VARCHAR(15))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        UPDATE PRODUCT
            SET
                ProductAvailability = newAvailability
            WHERE ProductID = product;

        RETURN 0;
    END;;

DROP FUNCTION IF EXISTS getProductName;

CREATE FUNCTION getProductName (product INT)
RETURNS VARCHAR(45)
READS SQL DATA
    BEGIN
        DECLARE productName VARCHAR(45);

        SELECT ProductName INTO productName
        FROM PRODUCT
        WHERE ProductID = product;

        RETURN productName;
    END;;

DROP FUNCTION IF EXISTS getProductImage;

CREATE FUNCTION getProductImage (product INT)
RETURNS VARBINARY(256)
READS SQL DATA
    BEGIN
        DECLARE productImage VARBINARY(256);

        SELECT ProductImage INTO productImage
        FROM PRODUCT
        WHERE ProductID = product;

        RETURN productImage;
    END;;

DROP FUNCTION IF EXISTS getProductDescription;

CREATE FUNCTION getProductDescription (product INT)
RETURNS VARCHAR(150)
READS SQL DATA
    BEGIN
        DECLARE productDesc VARCHAR(150);

        SELECT ProductDescription INTO productDesc
        FROM PRODUCT
        WHERE ProductID = product;

        RETURN productDesc;
    END;;

DROP FUNCTION IF EXISTS getProductAvailability;

CREATE FUNCTION getProductAvailability (product INT)
RETURNS VARCHAR(15)
READS SQL DATA
    BEGIN
        DECLARE productAvailability VARCHAR(15);

        SELECT ProductAvailability INTO productAvailability
        FROM PRODUCT
        WHERE ProductID = product;

        RETURN productAvailability;
    END;;

DROP FUNCTION IF EXISTS getProductPrice;

CREATE FUNCTION getProductPrice (product INT)
RETURNS FLOAT
READS SQL DATA
    BEGIN
        DECLARE productPrice FLOAT;

        SELECT Price INTO productPrice
        FROM PRODUCT
        WHERE ProductID = product;

        RETURN productPrice;
    END;;

DELIMITER ;