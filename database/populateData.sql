SELECT createOrg ("Test Organization", 0.10);

SELECT createDriver ("Test Driver", "driver@email.com", "driverPass", "42 Road Way, City, ST, 12345", "555-555-5555", 1);

SELECT createSponsor ("Test Sponsor", "sponsor@email.com", "sponsorPass", 5555555555555555, 123, 08/22, "1 Road Rd, City, ST, 12345", 1);

SELECT createAdmin ("Test Admin", "admin@email.com", "adminPass");

INSERT INTO POINT_CHANGE_REASON (ReasonDescription, OrgID)
    VALUES ("Test", 1);

INSERT INTO POINT_CHANGE (ChangeDate, ReasonID, NumPoints, TotalPoints, DriverID, SponsorID)
    VALUES ('2021-03-29', 1, 50, 100, 1, 2);

INSERT INTO POINT_CHANGE (ChangeDate, ReasonID, NumPoints, TotalPoints, DriverID, SponsorID)
    VALUES ('2021-03-05', 1, -50, 50, 1, 2);