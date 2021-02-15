INSERT INTO PASSWORD_CHANGE (ChangeNo, ChangeDate, ChangeType) VALUES (2, 2/13/2021, 'Reset');

INSERT INTO USER (UserID, Name, Email, HashedPassword, ChangeNo) VALUES (1, 'John Doe', 'johndoe@email.com', SHA('password'), 2);