from django.db import models
from mysql.connector import connect, Error

#database functions
def getDB():
    try:
        connection = connect(host = 'truckingdb.c9tkxb1tjvpp.us-east-1.rds.amazonaws.com', user = 'admin', password = 'accesstodb', database = 'DRIVER_DB', autocommit = True)
    
    except Error as err:
        print(err)

    else:
        return connection

def getCursor(connection):
    try:
        cursor = connection.cursor(buffered = True)
    
    except Error as err:
        print(err)
    
    else:
        return cursor

#sponsor functions
def acceptApplicant(userEmail, reasoning, password):
    accept_stmt = "SELECT acceptApplicant(%s, %s)"

    conn = getDB()
    cursor = getCursor(conn)

    args = (userEmail, reasoning, password)
    cursor.execute(accept_stmt, args)

    cursor.close()
    conn.close()


def rejectApplicant(userEmail, reasoning):
    reject_stmt = "SELECT rejectApplicant(%s, %s)"

    conn = getDB()
    cursor = getCursor(conn)

    args = (userEmail, reasoning)
    cursor.execute(reject_stmt, args)

    cursor.close()
    conn.close()

def giveDriverPoints(driverEmail, sponsorEmail, reason, points, date):
    givePoints_stmt = "SELECT manualPointChange(%s, %s, %s, %s, %s)"

    conn = getDB()
    cursor = getCursor(conn)

    args = (driverEmail, sponsorEmail, reason, points, date)
    cursor.execute(givePoints_stmt, args)

    cursor.close()
    conn.close()

def removeDriverPoints(driverEmail, sponsorEmail, reason, points, date):
    removePoints_stmt = "SELECT manualPointChange(%s, %s, %s, %s, %s)"

    conn = getDB()
    cursor = getCursor(conn)

    args = (driverEmail, sponsorEmail, reason, -1*points, date)
    cursor.execute(removePoints_stmt, args)

    cursor.close()
    conn.close()

# test function
# I used this to make sure I was making changes to the database
def testFunction():
    test_stmt = "SELECT createApplicant(%s, %s, %s, %s, %s, %s)"

    conn = getDB()
    cursor = getCursor(conn)

    args = ('2021-03-22', 'test_user', 'test_user@mail.com', '1234567890', '123 Street Rd.', '1')
    cursor.execute(test_stmt, args)

    cursor.close()
    conn.close()

# Create your models here.
