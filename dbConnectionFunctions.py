import datetime
from mysql.connector import connect, Error

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


def updateEmail(connection, cursor, newEmail, oldEmail):
    try:
        query = "SELECT emailExists(%s)"

        cursor.execute(query, (newEmail,))
        result = cursor.fetchone()

        for emailExists in result:
            if emailExists == 0:
                query = "SELECT updateEmail(%s, %s)"

                cursor.execute(query, (oldEmail, newEmail,))

                return "Email successfully updated."
            elif emailExists == 1:
                return "Email is already taken by another account."
    
    except Error as err:
        print (err)

def updatePassword(connection, cursor, email, newPassword):
    try:
        query = "SELECT emailExists(%s)"

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for emailExists in result:
            if emailExists == 1:
                query = "SELECT updatePassword(%s, %s)"
                cursor.execute(query, (email, newPassword,))

                return "Password successfully updated."
            else:
                return "Error updating password. (Email not found)"
    except Error as err:
        print(err)

def changePassword(connection, cursor, email, newPassword):
    try:
        query = "SELECT addPassChange(%s, \"Manual Change\", %s)"
        date = datetime.date.today()
        cursor.execute(query, (email, date))

        return updatePassword(connection, cursor, email, newPassword)
    except Error as err:
        print(err)

def resetPassword(connection, cursor, email, newPassword):
    try:
        query = "SELECT addPassChange(%s, \"Reset\", %s)"
        date = datetime.date.today()
        cursor.execute(query, (email, date))

        return updatePassword(connection, cursor, email, newPassword)
    except Error as err:
        print(err)

def firstPassword(connection, cursor, email, newPassword):
    try:
        query = "SELECT addPassChange(%s, \"First-Time\", %s)"
        date = datetime.date.today()
        cursor.execute(query, (email, date))

        return updatePassword(connection, cursor, email, newPassword)
    except Error as err:
        print(err)
        
#FIXME
def updateAddress(connection, cursor, email, newUserAddress, oldUserAddress):
    try:
        query = "SELECT emailExists(%s)"

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for emailExists in result:
            if emailExists == 1:
                query = "SELECT updateAddress(%s, %s, %s)"
                cursor.execute(query, (email, newUserAddress, oldUserAddress))
        
                return "Address successfully updated."
            else:
                return "Error updating address (Email not found)"
    except Error as err:
        print(err)

def addAddress(connection, cursor, email, newAddress):
    try:
        query = "SELECT emailExists(%s)"

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for emailExists in result:
            if emailExists == 1:
                query = "SELECT addAddress(%s, %s)"
                cursor.execute(query, (email, newAddress,))

                return "Address successfully added."
            else:
                return "Error updating address (Email not found)"
    
    except Error as err:
        print(err)

connection = getDB()
cursor = getCursor(connection)

print(updateEmail(connection, cursor, "johndoe@email.com", "jdoe@email.com"))
print(updatePassword(connection, cursor, "johndoe@email.com", "weakPass"))
print(updateAddress(connection, cursor, "johndoe@email.com", "42 Lane Ln, Springfield, NT, 12345", "42 Road LN, City, ST, 1234"))
print(addAddress(connection, cursor, "johndoe@email.com", "42 Road LN, City, ST, 12345"))

cursor.close()
connection.close()
