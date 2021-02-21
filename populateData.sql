INSERT INTO USER (UserID, Name, Email, HashedPassword) VALUES (1, 'John Doe', 'johndoe@email.com', SHA('password'));

INSERT INTO PASSWORD_CHANGE (ChangeNo, ChangeDate, ChangeType, UserID) VALUES (2, 2/13/2021, 'Reset', 1);

INSERT INTO DRIVER_ADDRESSES (UserID, Address) VALUES (1, "42 Road LN, City, ST, 1234");