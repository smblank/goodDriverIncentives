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

def checkEmail(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT emailExists(%s)"

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for emailExists in result:
            if emailExists == 0:
                cursor.close()
                conn.close()
                return False
            
            else:
                cursor.close()
                conn.close()
                return True
    except Error as err:
        print(err)


def updateEmail(newEmail, oldEmail):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(newEmail)

        if emailExists == False:
            query = "SELECT updateEmail(%s, %s)"

            cursor.execute(query, (oldEmail, newEmail,))

            cursor.close()
            conn.close()
            return "Email successfully updated."
        else:
            cursor.close()
            conn.close()
            return "Email is already taken by another account."
    
    except Error as err:
        print (err)

def updatePassword(email, newPassword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT updatePassword(%s, %s)"
            cursor.execute(query, (email, newPassword,))

            cursor.close()
            conn.close()
            return "Password successfully updated."
        else:
            cursor.close()
            conn.close()
            return "Error updating password. (Email not found)"
    except Error as err:
        print(err)

def changePassword(email, newPassword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addPassChange(%s, \"Manual Change\", %s)"
        date = datetime.date.today()
        cursor.execute(query, (email, date))

        cursor.close()
        conn.close()
        return updatePassword(email, newPassword)
    except Error as err:
        print(err)

def resetPassword(email, newPassword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addPassChange(%s, \"Reset\", %s)"
        date = datetime.date.today()
        cursor.execute(query, (email, date))

        cursor.close()
        conn.close()
        return updatePassword(email, newPassword)
    except Error as err:
        print(err)

def firstPassword(email, newPassword):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addPassChange(%s, \"First Time\", %s)"
        date = datetime.date.today()
        cursor.execute(query, (email, date))

        cursor.close()
        conn.close()
        return updatePassword(email, newPassword)
    except Error as err:
        print(err)
        
def updateAddress(email, newUserAddress, oldUserAddress):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT updateAddress(%s, %s, %s)"
            cursor.execute(query, (email, newUserAddress, oldUserAddress))
    
            cursor.close()
            conn.close()
            return "Address successfully updated."
        else:
            return "Error updating address (Email not found)"
    except Error as err:
        print(err)

def addAddress(email, newAddress):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT addAddress(%s, %s)"
            cursor.execute(query, (email, newAddress,))

            cursor.close()
            conn.close()
            return "Address successfully added."
        else:
            cursor.close()
            conn.close()
            return "Error updating address (Email not found)"
    
    except Error as err:
        print(err)

def setDefaultAddress(email, defaultAddr):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT setAddressDefault(%s, %s)"
            cursor.execute(query, (email, defaultAddr,))

            cursor.close()
            conn.close()
            return "Default address set."
        else:
            cursor.close()
            conn.close()
            return "Error setting default address (Email not found)"

    except Error as err:
        print(err)

def getDefaultAddress(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExits = checkEmail(email)

        if emailExists == True:
            query = "SELECT getDefaultAddress(%s)"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            for addr in result:
                cursor.close()
                conn.close()
                return addr
        else:
            cursor.close()
            conn.close()
            return "Error finding default address (Email not found)"
  
    except Error as err:
        print(err)

def getUserType(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getUserType(%s)"

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for userType in result:
            cursor.close()
            conn.close()
            return userType
    
    except Error as err:
        print(err)

def updatePhone(email, newPhone):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT updateDriverPhone(%s, %s)"

        cursor.execute(query, (email, newPhone,))

        cursor.close()
        conn.close()
        return "Phone number successfully updated."
    except Error as err:
        print(err)

def setProfilePic(email, picture):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        emailExists = checkEmail(email)

        if emailExists == True:
            query = "SELECT setProfilePic(%s, %s)"
            cursor.execute(query, (email, picture,))
    
            cursor.close()
            conn.close()
            return "Profile picture successfully updated."
        else:
            return "Error updating profile picture (Email not found)"

    except Error as err:
        print(err)