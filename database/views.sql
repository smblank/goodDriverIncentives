CREATE VIEW ADMINS AS
    SELECT USER.UserID, Name, Email
    FROM USER, ADMINISTRATOR
    WHERE USER.UserID = ADMINISTRATOR.UserID;

CREATE VIEW SPONSORS AS
    SELECT USER.UserID, Name, Email
    FROM USER, SPONSOR
    WHERE USER.UserID = SPONSOR.UserID;

CREATE VIEW DRIVERS AS
    SELECT USER.UserID, Name, Email
    FROM USER, DRIVER
    WHERE USER.UserID = DRIVER.UserID;