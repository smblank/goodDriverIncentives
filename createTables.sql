CREATE TABLE PASSWORD_CHANGE
    (ChangeNo INT NOT NULL,
    ChangeDate DATE NOT NULL,
    ChangeType VARCHAR(35) NOT NULL,
    PRIMARY KEY (ChangeNo));

CREATE TABLE USER
    (UserID        INT             NOT NULL,
    Name           VARCHAR(100)    NOT NULL,
    Email          VARCHAR(15)     NOT NULL,
    HashedPassword BINARY(64)     NOT NULL,
    ChangeNo    INT     NOT NULL,
    PRIMARY KEY (UserID),
    FOREIGN KEY (ChangeNo) REFERENCES PASSWORD_CHANGE (ChangeNo));

CREATE TABLE ADMINSTRATOR
    (UserID        INT             NOT NULL,
    PRIMARY KEY (UserID),
    FOREIGN KEY (UserID) REFERENCES USER (UserID));

CREATE TABLE ORG_CATALOG
    (CatalogID  INT     NOT NULL,
    PRIMARY KEY (CatalogID));

CREATE TABLE ORGANIZATION
    (OrgID      INT     NOT NULL,
    Logo        VARBINARY(256),
    PointConversion     FLOAT   NOT NULL,
    CatalogID       INT     NOT NULL,
    PRIMARY KEY (OrgID),
    FOREIGN KEY (CatalogID) REFERENCES ORG_CATALOG (CatalogID));

CREATE TABLE SPONSOR
    (UserID         INT         NOT NULL,
    CreditCardNum   INT,
    CreditCardSec   INT,
    CreditCardDate  DATE,
    BillingAddress  VARCHAR(100),
    OrgID       INT     NOT NULL,
    PRIMARY KEY (UserID),
    FOREIGN KEY (UserID) REFERENCES USER (UserID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));

CREATE TABLE DRIVER
    (UserID    INT     NOT NULL,
    Address     VARCHAR(100),
    PhoneNo    CHAR(12),
    Points      INT     NOT NULL,
    OrgID       INT     NOT NULL,
    PRIMARY KEY (UserID),
    FOREIGN KEY (UserID) REFERENCES USER (UserID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));

CREATE TABLE LOGIN_ATTEMPT
    (AttemptNo  INT     NOT NULL,
    AttemptDate        DATE    NOT NULL,
    Suceeded        BOOL        NOT NULL,
    UserID      INT     NOT NULL,
    PRIMARY KEY (AttemptNo),
    FOREIGN KEY (UserID) REFERENCES USER (UserID));

CREATE TABLE POINT_CHANGE_REASON
    (ReasonID       INT     NOT NULL,
    ReasonDescription   VARCHAR(50)     NOT NULL,
    PRIMARY KEY (ReasonID));

CREATE TABLE POINT_CHANGE
    (ChangeID       INT     NOT NULL,
    ChangeDate      DATE    NOT NULL,
    ReasonID    INT     NOT NULL,
    NumPoints      INT  NOT NULL,
    TotalPoints     INT     NOT NULL,
    UserID      INT     NOT NULL,
    SponsorID     INT    NOT NULL,
    PRIMARY KEY (ChangeID),
    FOREIGN KEY (UserID) REFERENCES USER (UserID),
    FOREIGN KEY (SponsorID) REFERENCES USER (USERID));

CREATE TABLE PRODUCT
    (ProductID      INT     NOT NULL,
    ProductName     VARCHAR(45)     NOT NULL,
    ProductImage    VARBINARY(256)  NOT NULL,
    ProductDescription  VARCHAR(150)    NOT NULL,
    ProductAvailability       VARCHAR(15)   NOT NULL,
    Price       INT     NOT NULL,
    PRIMARY KEY (ProductID));

CREATE TABLE IS_IN_CATALOG
    (CatalogID      INT     NOT NULL,
    ProductID       INT     NOT NULL,
    PRIMARY KEY (CatalogID, ProductID),
    FOREIGN KEY (CatalogID) REFERENCES ORG_CATALOG (CatalogID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID));

CREATE TABLE DRIVER_ORDER
    (OrderID      INT   NOT NULL,
    OrderDate       DATE    NOT NULL,
    PRIMARY KEY (OrderID));

CREATE TABLE IS_IN_ORDER
    (OrderID       INT      NOT NULL,
    ProductID       INT     NOT NULL,
    Quantity        INT     NOT NULL,
    PRIMARY KEY (OrderID, ProductID),
    FOREIGN KEY (OrderID) REFERENCES DRIVER_ORDER (OrderID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID));

CREATE TABLE BELONGS_TO
    (UserID     INT     NOT NULL,
    OrderID     INT     NOT NULL,
    PRIMARY KEY (UserID, OrderID),
    FOREIGN KEY (UserID) REFERENCES USER (UserID),
    FOREIGN KEY (OrderID) REFERENCES DRIVER_ORDER (OrderID));

CREATE TABLE WISHLIST
    (ListID       INT   NOT NULL,
    UserID      INT     NOT NULL,
    PRIMARY KEY (ListID),
    FOREIGN KEY (UserID) REFERENCES USER (UserID));

CREATE TABLE IS_IN_WISHLIST
    (ProductID      INT     NOT NULL,
    ListID      INT     NOT NULL,
    PRIMARY KEY (ProductID, ListID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID),
    FOREIGN KEY (ListID) REFERENCES WISHLIST (ListID));

CREATE TABLE APPLICANT
    (ApplicantID    INT     NOT NULL,
    ApplicantDate   DATE    NOT NULL,
    IsAccepted      BOOL    NOT NULL,
    Reason      VARCHAR(150)    NOT NULL,
    ApplicantName   VARCHAR(100)    NOT NULL,
    PhoneNo     CHAR(12)    NOT NULL,
    HomeAddress     VARCHAR(100)    NOT NULL,
    EmployeeID      INT     NOT NULL,
    OrgID       INT     NOT NULL,
    PRIMARY KEY (ApplicantID),
    FOREIGN KEY (OrgID) REFERENCES ORGANIZATION (OrgID));