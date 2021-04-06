from django.db import models
from django.shortcuts import render
import os
import dbConnectionFunctions as db
from orgPage import views

# Create your models here.
def getNewLogo(request):
    newLogo = request.FILES['logo']
    extension = os.path.splitext(newLogo.name)[1]

    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    imgPath = 'static/img/' + 'user' + str(db.getOrgName(orgNo)) + extension
    response = db.setOrgLogo(orgNo, str(db.getOrgName(orgNo)) + extension)

    with open(imgPath, 'wb+') as f:
        for chunk in newLogo.chunks():
            f.write(chunk)

    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def getNewPointChange(request):
    numPoints = request.POST.get('numPoints')
    desc = request.POST.get('description')

    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    db.addPointChangeReason(desc, numPoints, orgNo)
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def updatePointConversion(request):
    dollarAmt = request.POST.get('dollars')
    pointAmt = request.POST.get('points')

    newConversion = float(dollarAmt) / float(pointAmt)
    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    db.updatePointConversion(orgNo, newConversion)
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def updatePaymentInfo(request):
    ccName = request.POST.get('ccName')
    ccNum = request.POST.get('ccNum')
    ccSec = request.POST.get('ccSec')
    ccDate = request.POST.get('ccDate')
    addr1 = request.POST.get('addr1')
    addr2 = request.POST.get('addr2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip = request.POST.get('zip')

    address = addr1
    if (addr2 != ''):
        address += ' ' + addr2
    address += ', ' + city + ', ' + state + ' ' + zip

    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    db.updateOrgPayment(int(ccNum), int(ccSec), ccDate, address, orgNo, 1)
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def addNewSponsor(request):
    email = request.POST.get('email')
    name = request.POST.get('name')

    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    elif (request.session['isAdmin']):
        orgNo = request.session['adminOrgChoice']
    else:
        orgNo = db.getOrgNo(request.session['email'])

    newPassword = db.getRandomPassword()

    db.createSponsor(name, email, newPassword, orgNo)

    db.emailNewSponsor(email, newPassword, orgNo)

    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def removeReason(request):
    reasonID = request.POST.get('reason')

    db.removePointChangeReason(reasonID)    
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

# Not fully implemented
def editReason(request):
    reasonID = request.POST.get('reason')
    print(reasonID)
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def removeSponsor(request):
    sponsorID = request.POST.get('sponsor')

    currUserID = db.getUserID(request.session['email'])

    if (sponsorID != currUserID):
        db.removeSponsor(sponsorID, currUserID)
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def removeDriver(request):
    driverID = request.POST.get('driver')

    db.removeDriver(driverID)
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)

def getAdminOrgChoice(request):
    orgChoice = request.POST.get('orgs')

    request.session['adminOrgChoice'] = orgChoice
    if (request.session['isAdmin']):
        return views.adminOrgs(request)
    else:
        return views.organizationPage(request)
    