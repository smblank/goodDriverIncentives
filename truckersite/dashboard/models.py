from django.db import models
import dbConnectionFunctions as db
from dashboard import views
from sponsor import views as spon

# Create your models here.
def removeDriver(request):
    userType = db.getUserType(request.session['email'])

    email = request.POST.get('email')

    db.removeDriver(email)
    
    if userType == "Sponsor":
        return views.sponsorDash(request)

    elif userType == 'Admin':
        return views.adminDash(request)

def removeSponsor(request):
    userType = db.getUserType(request.session['email'])

    email = request.POST.get('email')

    db.removeSponsor(email, request.session['email'])

    if userType == "Sponsor":
        return views.sponsorDash(request)

    elif userType == 'Admin':
        return views.adminDash(request)

def removeAdmin(request):
    email = request.POST.get('email')

    db.removeAdmin(email)

    return views.adminDash(request)

def updateLogin(request):
    user = request.POST.get('oldEmail')
    newEmail = request.POST.get('newEmail')
    newPassword = request.POST.get('newPass')

    if newEmail != '':
        db.updateEmail(user, newEmail)
    
    if newPassword != '':
        db.updatePassword(user, newPassword)

    return views.adminDash(request)

def setDriverView(request):
    tempEmail = 'temp@email.com'
    request.session['tempEmail'] = tempEmail
    request.session['isViewing'] = True

    request.session['tempId'] = db.createTempDriver(tempEmail, 1)
    
    return views.driverDash(request)

def setSponsorView(request):
    tempEmail = 'temp@email.com'
    request.session['tempEmail'] = tempEmail
    request.session['isViewing'] = True

    request.session['tempId'] = db.createTempSponsor(tempEmail, 1)
    
    return spon.sponsorDashDisplay(request)

def revertDriverView(request):
    db.removeTempDriver(request.session['tempId'])
    del request.session['tempEmail']
    del request.session['tempId']

    request.session['isViewing'] = False

    return views.adminDash(request)

def revertSponsorView(request):
    db.removeTempSponsor(request.session['tempId'])
    del request.session['tempEmail']
    del request.session['tempId']

    request.session['isViewing'] = False

    return views.adminDash(request)