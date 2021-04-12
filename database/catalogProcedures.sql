DELIMITER ;;

DROP FUNCTION IF EXISTS getDriverPoints;

CREATE FUNCTION getDriverPoints(driverEmail VARCHAR(50), orgID INT)
RETURNS INT
READS SQL DATA
    BEGIN
        DECLARE driver INT;
        DECLARE pointTotal INT;

        SELECT getUserID(driverEmail) INTO driver;

        SELECT Points INTO pointTotal
        FROM DRIVER_ORGS
        WHERE UserID = driver AND OrgID = orgID;

        RETURN pointTotal;
    END;;

DROP FUNCTION IF EXISTS createProduct;

CREATE FUNCTION createProduct (id CHAR(12), name VARCHAR(100), price FLOAT, img VARCHAR(250))
RETURNS CHAR(12)
MODIFIES SQL DATA
    BEGIN
        DECLARE newProduct INT;

        INSERT INTO PRODUCT (ProductID, ProductName, Price, ImgUrl)
        VALUES (id, name, price, img);

        SELECT ProductId INTO newProduct
        FROM PRODUCT
        WHERE ProductID = @@Identity;

        RETURN newProduct;
    END;;

DROP PROCEDURE IF EXISTS getProduct;

CREATE PROCEDURE getProduct (id CHAR(12))
    BEGIN
        SELECT ProductName, Price, ImgUrl
        FROM PRODUCT
        WHERE ProductID = id;
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

DROP PROCEDURE IF EXISTS getProductsInCatalog;

CREATE PROCEDURE getProductsInCatalog(org INT)
    BEGIN
        SELECT PRODUCT.ProductID, ProductName, Price, ImgUrl
        FROM PRODUCT, IS_IN_CATALOG, ORGANIZATION
        WHERE ORGANIZATION.CatalogID = IS_IN_CATALOG.CatalogID AND
                PRODUCT.ProductID = IS_IN_CATALOG.ProductID;
    END;;

DROP FUNCTION IF EXISTS addToCatalog;

CREATE FUNCTION addToCatalog (product CHAR(12), org INT)
RETURNS BOOLEAN
MODIFIES SQL DATA
    BEGIN
        DECLARE productExists BOOLEAN;
        DECLARE catalogue INT;

        SELECT CatalogID INTO catalogue
        FROM ORGANIZATION
        WHERE OrgID = org;

        
        INSERT INTO IS_IN_CATALOG (CatalogID, ProductID) VALUES (catalogue, product);

        RETURN productExists;
    END;;

DROP PROCEDURE IF EXISTS clearCatalog;

CREATE PROCEDURE clearCatalog(orgNo INT)
    BEGIN
        DECLARE catalogue INT;

        SELECT CatalogID INTO catalogue
        FROM ORGANIZATION
        WHERE OrgID = orgNo;

        DELETE FROM IS_IN_CATALOG
        WHERE CatalogID = catalogue;
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

        INSERT INTO DRIVER_ORDER (OrderDate, Status) VALUES (dateCreated, 'In-Progress');

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

DROP FUNCTION IF EXISTS completeOrder;

CREATE FUNCTION completeOrder(completeDate DATE, orderID INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        UPDATE DRIVER_ORDER
            SET
                OrderDate = completeDate,
                Status = 'Delivered'
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

DROP PROCEDURE IF EXISTS getDriverOrders;

CREATE PROCEDURE getDriverOrders(driver INT, org INT)
    BEGIN
        SELECT DRIVER_ORDER.OrderID, OrderDate, ProductName, Quantity, Price, Status
        FROM DRIVER_ORDER, IS_IN_ORDER, BELONGS_TO, PRODUCT
        WHERE BELONGS_TO.DriverID = driver AND
                BELONGS_TO.OrderID = DRIVER_ORDER.OrderID  AND IS_IN_ORDER.OrderID = BELONGS_TO.OrderID AND
                IS_IN_ORDER.ProductID = PRODUCT.ProductID AND
                Status != 'In-Progress';
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

CREATE FUNCTION getProductName (product CHAR(12))
RETURNS VARCHAR(100)
READS SQL DATA
    BEGIN
        DECLARE productName VARCHAR(100);

        SELECT ProductName INTO productName
        FROM PRODUCT
        WHERE ProductID = product;

        RETURN productName;
    END;;

DROP FUNCTION IF EXISTS getProductImage;

CREATE FUNCTION getProductImage (product CHAR(12))
RETURNS VARCHAR(200)
READS SQL DATA
    BEGIN
        DECLARE productImage VARCHAR(200);

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

DROP FUNCTION IF EXISTS getProductPrice;

CREATE FUNCTION getProductPrice (product CHAR(12))
RETURNS FLOAT
READS SQL DATA
    BEGIN
        DECLARE productPrice FLOAT;

        SELECT Price INTO productPrice
        FROM PRODUCT
        WHERE ProductID = product;

        RETURN productPrice;
    END;;

DROP FUNCTION IF EXISTS changePointTotal;

CREATE FUNCTION changePointTotal (driverEmail VARCHAR(50), pointChange INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newTot INT;
        DECLARE driver INT;

        SELECT getUserID(driverEmail) INTO driver;

        UPDATE DRIVER
            SET Points = Points + pointChange
            WHERE UserID = driver;

        SELECT Points INTO newTot
        FROM DRIVER
        WHERE UserID = driver;

        RETURN newTot;
    END;;

DROP FUNCTION IF EXISTS manualPointChange;

CREATE FUNCTION manualPointChange (driverEmail VARCHAR(50), sponsorEmail VARCHAR(50), reason VARCHAR(100), pointChange INT, changeDate DATE)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newTot INT;
        DECLARE driver INT;
        DECLARE sponsor INT;
        DECLARE reasonID INT;

        SELECT getUserID(driverEmail) INTO driver;
        SELECT getUserID(sponsorEmail) INTO sponsor;

        SELECT ReasonID INTO reasonID
        FROM POINT_CHANGE_REASON
        WHERE ReasonDescription = reason;

        SELECT changePointTotal(driverEmail, pointChange) INTO newTot;

        INSERT INTO POINT_CHANGE (ChangeDate, ReasonID, NumPoints, TotalPoints, DriverID, SponsorID)
        VALUES (changeDate, reasonID, pointChange, newTot, driver, sponsor);

        RETURN newTot;
    END;;

DROP FUNCTION IF EXISTS addOrgPayment;

CREATE FUNCTION addOrgPayment (ccNum INT, ccSec INT, ccDate DATE, billAddr VARCHAR(100), organization INT)
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newPayment INT;

        INSERT INTO ORG_PAYMENTS (CreditCardNum, CreditCardSec, CreditCardDate, BillingAddress, OrgID)
            VALUES (ccNum, ccSec, ccDate, billAddr, organization);
        
        SELECT PayID INTO newPayment
        FROM ORG_PAYMENTS
        WHERE PayID = @@Identity;

        RETURN newPayment;
    END;;

DROP PROCEDURE IF EXISTS updateOrgPayment;

CREATE PROCEDURE updateOrgPayment (ccNum INT, ccSec INT, ccDate DATE, billAddr VARCHAR(100), organization INT, payID INT)
    BEGIN
        UPDATE ORG_PAYMENTS
            SET
                CreditCardNum = ccNum,
                CreditCardSec = ccSec,
                CreditCardDate = ccDate,
                BillingAddress = billAddr
        WHERE PayID = payID AND OrgID = organization;
    END;;

DROP PROCEDURE IF EXISTS getKeywords;

CREATE PROCEDURE getKeywords(org INT)
READS SQL DATA
    BEGIN
        DECLARE catalogue INT;

        SELECT CatalogID INTO catalogue
        FROM ORGANIZATION
        WHERE OrgID = org;

        SELECT WordID, Keyword
        FROM CATALOG_KEYWORDS
        WHERE CatalogID = catalogue;
    END;;

DROP FUNCTION IF EXISTS addKeyword;

CREATE FUNCTION addKeyword (org INT, newKeyword VARCHAR(20))
RETURNS INT
MODIFIES SQL DATA
    BEGIN
        DECLARE newWord INT;
        DECLARE catalogue INT;

        SELECT CatalogID INTO catalogue
        FROM ORGANIZATION
        WHERE OrgID = org;

        INSERT INTO CATALOG_KEYWORDS (CatalogID, Keyword)
            VALUES (catalogue, newKeyword);

        SELECT WordID INTO newWord
        FROM CATALOG_KEYWORDS
        WHERE WordID = @@Identity;

        RETURN newWord;
    END;;

DROP PROCEDURE IF EXISTS removeKeyword;

CREATE PROCEDURE removeKeyword (org INT, word INT)
    BEGIN
        DECLARE catalogue INT;

        SELECT CatalogID INTO catalogue
        FROM ORGANIZATION
        WHERE OrgID = org;

        DELETE FROM CATALOG_KEYWORDS
            WHERE CatalogID = catalogue AND WordID = word;
    END;;

DELIMITER ;