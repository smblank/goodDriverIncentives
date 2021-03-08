INSERT INTO USER (UserID, Name, Email, HashedPassword) VALUES (1, 'John Doe', 'johndoe@email.com', SHA('password'));

INSERT INTO ORG_CATALOG (CatalogID) VALUES (1);

INSERT INTO ORGANIZATION (OrgID, Name, Pointconversion, CatalogID) VALUES (1, "Organization", 0.10, 1);

SELECT createDriver("Jane Doe", "jane@example.com", "password", "temp address", "123-456-7890", 1);

INSERT INTO PASSWORD_CHANGE (ChangeNo, ChangeDate, ChangeType, UserID) VALUES (2, 2/13/2021, 'Reset', 1);

INSERT INTO DRIVER_ADDRESSES (UserID, Address, DefaultAddr) VALUES (1, "42 Road LN, City, ST, 1234", False);