from datetime import datetime
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

def getUserID(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getUserID(%s)"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for userID in result:
            cursor.close()
            conn.close()
            return userID

    except Error as err:
        print(err)

def getUserEmail(id):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getUserEmail(%s)"
        cursor.execute(query, (id,))
        result = cursor.fetchone()

        for userEmail in result:
            cursor.close()
            conn.close()
            return userEmail

    except Error as err:
        print(err)

def getDriverPoints(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getDrivePoints(%s)"
        cursor.exectue(query, (email))
        result = cursor.fetchone()

        for points in result:
            cursor.close()
            conn.close()
            return points
    
    except Error as err:
        print(err)

def checkPassword (email, password):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT checkPassword(%s, %s)"
        cursor.execute(query, (email, password,))
        result = cursor.fetchone()

        for correctPassword in result:
            cursor.close()
            conn.close()
            return correctPassword

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

def checkIsInCatalog (productID, catalogID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT isInCatalog(%s, %s)"
        cursor.execute(query, (productID, catalogID,))
        result = cursor.fetchone()

        for inCatalog in result:
            cursor.close()
            conn.close()
            return inCatalog

    except Error as err:
        print(err)

def addToCatalog (productID, catalogID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addToCatalog(%s, %s)"
        cursor.execute(query, (productID, catalogID,))

        cursor.close()
        conn.close()
        return "Product successfuly added to catalog"
    
    except Error as err:
        print(err)

def removeToCatalog (productID, catalogID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeFromCatalog(%s, %s)"
        cursor.execute(query, (productID, catalogID,))
        result = cursor.fetchone()

        for success in result:
            if success == True:
                cursor.close()
                conn.close()
                return "Product successfuly removed from catalog"

            else:
                cursor.close()
                conn.close()
                return "Error removing product (product or catalog does not exist)"
    
    except Error as err:
        print(err)

def createOrder (driverID, date):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createOrder(%s, %s)"
        cursor.execute(query, (driverID, date,))
        result = cursor.fetchone()

        for orderID in result:
            cursor.close()
            conn.close()
            return orderID
    
    except Error as err:
        print(err)

def cancelOrder (orderID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT cancelOrder(%s)"
        cursor.execute(query, (orderID,))

        cursor.close()
        conn.close()
        return "Order successfully canceled"
    
    except Error as err:
        print(err)

def completeOrder (orderID, completeDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT completeOrder(%s, %s)"
        cursor.execute(query, (orderID, completeDate))

        cursor.close()
        conn.close()
        return "Order successfully completed"
    
    except Error as err:
        print(err)


def addToOrder (orderID, productID, amt):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addToOrder(%s, %s, %s)"
        cursor.execute(query, (orderID, productID, amt,))

        cursor.close()
        conn.close()
        return "Product successfuly added to order"
    
    except Error as err:
        print(err)

def removeFromOrder (orderID, productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeFromOrder(%s, %s)"
        cursor.execute(query, (orderID, productID,))

        cursor.close()
        conn.close()
        return "Product successfuly removed from catalog"
    
    except Error as err:
        print(err)

def updateQuantityInOrder (orderID, productID, newAmt):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT updateQuantity(%s, %s, %s)"
        cursor.execute(query, (orderID, productID, newAmt,))

        cursor.close()
        conn.close()
        return "Quantity successfully updated"
    
    except Error as err:
        print(err)

def checkIsInOrder (orderID, productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT isInOrder(%s, %s)"
        cursor.execute(query, (orderID, productID,))
        result = cursor.fetchone()

        for inOrder in result:
            cursor.close()
            conn.close()
            return inOrder
    
    except Error as err:
        print(err)

def addToWishlist (driverID, productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT addToWishlist(%s, %s)"
        cursor.execute(query, (driverID, productID,))

        cursor.close()
        conn.close()
        return "Product successfuly added to wishlist"
    
    except Error as err:
        print(err)

def removeFromWishlist (driverID, productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeFromWishlist(%s, %s)"
        cursor.execute(query, (driverID, productID,))

        cursor.close()
        conn.close()
        return "Product successfuly removed from wishlist"
    
    except Error as err:
        print(err)

def checkIsInWishlist (driverID, productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT isInWishlist(%s, %s)"
        cursor.execute(query, (driverID, productID,))
        result = cursor.fetchone()

        for inWishlist in result:
            cursor.close()
            conn.close()
            return inWishlist
    
    except Error as err:
        print(err)

def updatePrice (productID, newPrice):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT updatePrice(%s, %s)"
        cursor.execute(query, (productID, newPrice,))

        cursor.close()
        conn.close()
        return "Product price successfully updated"

    except Error as err:
        print(err)

def updateAvailability (productID, newAvailability):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT updateAvailability(%s, %s)"
        cursor.execute(query, (productID, newAvailability,))

        cursor.close()
        conn.close()
        return "Product availability successfully updated"

    except Error as err:
        print(err)

def getProductName (productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getProductName(%s)"
        cursor.execute(query, (productID,))
        result = cursor.fetchone()

        for productName in result:
            cursor.close()
            conn.close()
            return productName

    except Error as err:
        print(err)

def getProductImage (productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getProductImage(%s)"
        cursor.execute(query, (productID,))
        result = cursor.fetchone()

        for productImage in result:
            cursor.close()
            conn.close()
            return productImage

    except Error as err:
        print(err)

def getProductDescription (productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getProductDescription(%s)"
        cursor.execute(query, (productID,))
        result = cursor.fetchone()

        for productDesc in result:
            cursor.close()
            conn.close()
            return productDesc

    except Error as err:
        print(err)

def getProductAvailability (productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getProductAvailability(%s)"
        cursor.execute(query, (productID,))
        result = cursor.fetchone()

        for productAvailability in result:
            cursor.close()
            conn.close()
            return productAvailability

    except Error as err:
        print(err)

def getProductPrice (productID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getProductPrice(%s)"
        cursor.execute(query, (productID,))
        result = cursor.fetchone()

        for productPrice in result:
            cursor.close()
            conn.close()
            return productPrice

    except Error as err:
        print(err)

def adjustPoints (driverEmail, sponsorEmail, reason, amt):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT manualPointChange(%s, %s, %s, %s, %s)"

        changeDate = datetime.date.today()
        cursor.execute(query, (driverEmail, sponsorEmail, reason, amt, changeDate))
        result = cursor.fetchone()

        for newTotal in result:
            cursor.close()
            conn.close()
            return newTotal

    except Error as err:
        print(err)

def spendPoints (driverEmail, cost):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT changePointTotal(%s, %s)"
        cursor.execute(query, (driverEmail, cost))
        result = cursor.fetchone()

        for newTotal in result:
            cursor.close()
            conn.close()
            return newTotal

    except Error as err:
        print(err)

def getRandomPassword():
    #Generate a random password that is 20 characters long
    randPassword = ''
    for _ in range(20):
        randPassword = randPassword + random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)

    return randPassword

def getOrgNo (userEmail):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getOrgNo(%s)"
        cursor.execute(query, (userEmail,))
        result = cursor.fetchone()

        for orgNo in result:
            cursor.close()
            conn.close()
            return orgNo

    except Error as err:
        print(err)

def getOrgName (orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getOrgName(%s)"
        cursor.execute(query, (orgID))
        result = cursor.fetchone()

        for orgName in result:
            cursor.close()
            conn.close()
            return orgName

    except Error as err:
        print(err)

def createDriver(name, email, password, address, phone, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createDriver(%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, address, phone, orgNo))

        return "Driver successfully created" 

    except Error as err:
        print(err)

def createSponsor(name, email, password, ccNum, ccSec, ccDate, billAddr, orgNo):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createDriver(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (name, email, password, ccNum, ccSec, ccDate, billAddr, orgNo))
        
        cursor.close()
        conn.close()
        return "Sponsor successfully created" 

    except Error as err:
        print(err)

def createAdmin(name, email, password):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createDriver(%s, %s, %s)"
        cursor.execute(query, (name, email, password))

        cursor.close()
        conn.close()
        return "Admin successfully created" 

    except Error as err:
        print(err)

def createApplicant(date, name, email, phone, orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT createApplicant(%s, %s, %s, %s, %s)"
        cursor.execute(query, (date, name, email, phone, orgID))
        result = cursor.fetchone()

        for applicantID in result:
            cursor.close()
            conn.close()
            return applicantID
        
    except Error as err:
        print(err)

def acceptApplicant(email, reasoning, password, acceptDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT acceptApplicant(%s, %s, %s, %s)"
        cursor.execute(query, (email, reasoning, password, acceptDate))
        result = cursor.fetchone()

        for driverID in result:
            cursor.close()
            conn.close()
            return driverID
        
    except Error as err:
        print(err)

def rejectApplicant(email, reasoning, rejectDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT rejectApplicant(%s, %s, %s)"
        cursor.execute(query, (email, reasoning, acceptDate))

        cursor.close()
        conn.close()
        return "Applicant successfully rejected"
        
    except Error as err:
        print(err)

def removeDriver(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeDriver(%s)"
        cursor.execute(query, (email,))

        cursor.close()
        conn.close()
        return "Driver successfully deleted" 

    except Error as err:
        print(err)

def removeSponsor (email, newSponsor):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeSponsor(%s, %s)"
        cursor.execute(query, (email, newSponsor))

        cursor.close()
        conn.close()
        return "Sponsor successfully deleted" 

    except Error as err:
        print(err)

def removeAdmin(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT removeAdmin(%s)"
        cursor.execute(query, (email,))

        cursor.close()
        conn.close()
        return "Admin successfully deleted" 

    except Error as err:
        print(err)

def getProfilePic(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getProfilePic(%s)"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for profilePic in result:
            cursor.close()
            conn.close()
            return profilePic

    except Error as err:
        print(err)

def getUserName(email):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "SELECT getUserName(%s)"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for name in result:
            cursor.close()
            conn.close()
            return name

    except Error as err:
        print(err)

def indvDriverPointChangeReport(startDate, endDate, orgID, driverID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL indvDriverPointChangeRep(%s, %s, %s, %s)"
        cursor.execute(query, (startDate, endDate, orgID, driverID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def allDriverPointChangeReport(startDate, endDate, orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        start = datetime.strptime(startDate, '%m/%d/%y').date()
        end = datetime.strptime(endDate, '%m/%d/%y').date()

        query = "CALL allDriverPointChangeRep(%s, %s, %s)"
        cursor.execute(query, (start, end, orgID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def indvSponsorSaleReport(startDate, endDate, detailed, driverID, orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL indvSponsorSaleRep(%s, %s, %s, %s, %s)"
        cursor.execute(query, (startDate, endDate, detailed, driverID, orgID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def allSponsorSaleReport(startDate, endDate, detailed):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL allSponsorSaleRep(%s, %s, %s)"
        cursor.execute(query, (startDate, endDate, detailed))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def driverSaleReport(startDate, endDate, detailed, orgID, driverID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL driverSaleRep(%s, %s, %s, %s, %s)"
        cursor.execute(query, (startDate, endDate, detailed, orgID, driverID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def indvSponsorInvoice(startDate, endDate, orgID):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL indvSponsorInvoice(%s, %s, %s)"
        cursor.execute(query, (startDate, endDate, orgID))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def allSponsorInvoice(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL allSponsorInvoice(%s, %s)"
        cursor.execute(query, (startDate, endDate))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def driverApplicationsReport(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL driverApplicationsRep(%s, %s)"
        cursor.execute(query, (startDate, endDate))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def pointChangeReport(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL pointChangeRep(%s, %s)"
        cursor.execute(query, (startDate, endDate))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def passwordChangeReport(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL passwordChangeRep(%s, %s)"
        cursor.execute(query, (startDate, endDate))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)

def loginAttemptsReport(startDate, endDate):
    try:
        conn = getDB()
        cursor = getCursor(conn)

        query = "CALL loginAttemptsRep(%s, %s)"
        cursor.execute(query, (startDate, endDate))
        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

    except Error as err:
        print(err)