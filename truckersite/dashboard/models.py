from django.db import models
import dbConnectionFunctions as db
from dashboard import views
from sponsor import views as spon

# Create your models here.

def getDriverOrg(request):
    orgID = request.POST.get('driverOrg')
    request.session['orgID'] = orgID
    return views.driverDash(request)

def removeAdmin(request):
    admin = request.POST.get('admin')

    db.removeAdmin(admin)

    return views.adminDash(request)

def addNewAdmin(request):
    email = request.POST.get('email')
    name = request.POST.get('name')

    newPassword = db.getRandomPassword()

    db.createAdmin(name, email, newPassword)

    db.emailNewAdmin(email, newPassword)

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