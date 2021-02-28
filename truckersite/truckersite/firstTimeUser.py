import datetime
from mysql.connector import connect, Error
import random
import string
from django.core.mail import EmailMessage

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

def getRandomPassword(userEmail):
    #Generate a random password that is 20 characters long
    randPassword = ''
    for _ in range(20):
        randPassword = randPassword + random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)

    return randPassword

def firstTimeEmail(userEmail):
    password = getRandomPassword(userEmail)

    query = "SELECT getUserName(%s)"

    conn = getDB()
    cursor = getCursor(conn)

    cursor.execute(query, (userEmail, ))
    result = cursor.fetchone()

    for userName in result:
        userName = userName
    
    subject = "Acceptance to the Good Driver Incentive Program"

    message = """\
    Welcome %s!
    
    Congratualations! You've been accepted into the Good Dirvers Incentive Program. Once you login for the first time, you'll be able to create your own password and start earning points. For your first login, please use this temporary password: %s. Welcom to the Program!
    
    Login Link: http://ec2-3-88-207-55.compute-1.amazonaws.com/""" % (userName,password)

    #Send email
    email = EmailMessage(subject, message, 'gooddriverprogram@gmail.com', [userEmail])
    email.send()

getRandomPassword("email")
firstTimeEmail("smblankenship99@gmail.com")