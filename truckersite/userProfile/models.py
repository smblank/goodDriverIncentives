from django.db import models
from django.shortcuts import render
import dbConnectionFunctions as db
from userProfile import views

def checkPhone(phoneNo):
    digits = ''

    #Get all numbers
    for char in phoneNo:
        if char.isdigit():
            digits += char

    if len(digits) != 10:
        return False
    
    else:
        return True

def formatPhone(phoneNo):
    digits = ''
    formattedNum = ''

    #Get all numbers
    for char in phoneNo:
        if char.isdigit():
            digits += char

    #Add dashes to number for readability       
    if len(digits) == 10:
        i = 0
        for num in digits:
            if i == 3:
                formattedNum += '-'
            elif i == 6:
                formattedNum += '-'
            formattedNum += num
            i += 1

    return formattedNum


def getNewDriverEmail(request):
    newEmail = request.POST.get('email')
    response = db.updateEmail(newEmail, request.session['email'])
    return render(request, 'driver_profile.html')

def getNewDriverPhone(request):
    newPhone = request.POST.get('phone')

    validPhone = checkPhone(newPhone)

    if validPhone == True:
        newPhone = formatPhone(newPhone)
        response = db.updatePhone(request.session['email'], newPhone)
    
    else:
        response = "Sorry that is not a valid phone number (ex. 555-555-5555)"

    return render(request, 'driver_profile.html')

def getNewDriverPassword(request):
    newPass = request.POST.get('password1')
    confirmPass = request.POST.get('password2')

    if newPass != confirmPass:
        response = "The passwords do not match."
        return render(request, 'driver_profile.html')
    
    response = db.changePassword(request.session['email'], newPass)

    return render(request, 'driver_profile.html')

def getNewDriverAddress(request):
    addr1 = request.POST.get('address1')
    addr2 = request.POST.get('address2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip = request.POST.get('zip')

    newAddr = addr1
    if addr2 != '':
        newAddr += ' ' + addr2
    newAddr += ', ' + city + ', ' + state + ' ' + zip

    response = db.addAddress(request.session['email'], newAddr)

    return views.driverProfile(request)

def getDriverDefaultAddr(request):
    defaultAddr = request.POST.get('default')

    response = db.setDefaultAddress(request.session['email'], defaultAddr)

    return views.driverProfile(request)

def getDriverProfilePic(request):
    profilePic = request.POST.get('profilePic')

    response = db.setProfilePic(request.session['email'], profilePic)

    return views.driverProfile(request)



def getNewSponsorEmail(request):
    newEmail = request.POST.get('email')
    response = db.updateEmail(newEmail, request.session['email'])
    return render(request, 'sponsor_profile.html')

def getNewSponsorPhone(request):
    newPhone = request.POST.get('phone')

    validPhone = checkPhone(newPhone)

    if validPhone == True:
        newPhone = formatPhone(newPhone)
        response = db.updatePhone(request.session['email'], newPhone)
    
    else:
        response = "Sorry that is not a valid phone number (ex. 555-555-5555)"

    return render(request, 'sponsor_profile.html')

def getNewSponsorPassword(request):
    newPass = request.POST.get('password1')
    confirmPass = request.POST.get('password2')

    if newPass != confirmPass:
        response = "The passwords do not match."
        return render(request, 'sponsor_profile.html')
    
    response = db.changePassword(request.session['email'], newPass)

    return render(request, 'sponsor_profile.html')

def getSponsorProfilePic(request):
    profilePic = request.POST.get('profilePic')

    response = db.setProfilePic(request.session['email'], profilePic)

    return views.sponsorProfile(request)




def getNewAdminEmail(request):
    newEmail = request.POST.get('email')
    response = db.updateEmail(newEmail, request.session['email'])
    return render(request, 'admin_profile.html')

def getNewAdminPassword(request):
    newPass = request.POST.get('password1')
    confirmPass = request.POST.get('password2')

    if newPass != confirmPass:
        response = "The passwords do not match."
        return render(request, 'admin_profile.html')
    
    response = db.changePassword(request.session['email'], newPass)

    return render(request, 'admin_profile.html')

def getAdminProfilePic(request):
    profilePic = request.POST.get('profilePic')

    response = db.setProfilePic(request.session['email'], profilePic)

    return views.adminProfile(request)




def createNewDriver(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    addr1 = request.POST.get('addr1')
    addr2 = request.POST.get('addr2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip = request.POST.get('zip')

    newAddr = addr1
    if addr2 != '':
        newAddr += ' ' + addr2
    newAddr += ', ' + city + ', ' + state + ' ' + zip

    newPhone = request.POST.get('phone')
    newPassword = db.getRandomPassword()
    userType = db.getUserType(request.session['email'])

    if userType == 'Sponsor':
        orgNo = db.getOrgNo(request.session['email'])
        db.createDriver(name, email, newPassword, newAddr, newPhone, orgNo)
        return views.sponsorProfile(request)

    elif userType == 'Admin':
        orgNo = request.POST.get('org')
        db.createDriver(name, email, newPassword, newAddr, newPhone, orgNo)
        return views.adminProfile(request)

def createNewSponsor(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = db.getRandomPassword()
    ccNum = request.POST.get('ccNum')
    ccSec = request.POST.get('ccSec')
    ccDate = request.POST.get('ccDate')
    addr1 = request.POST.get('addr1')
    addr2 = request.POST.get('addr2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip = request.POST.get('state')

    newAddr = addr1
    if addr2 != '':
        newAddr += ' ' + addr2
    newAddr += ', ' + city + ', ' + state + ' ' + zip

    userType = db.getUserType(request.session['email'])

    if userType == 'Sponsor':
        orgNo = db.getOrgNo(reqest.session['email'])
        db.createSponsor(name, email, password, ccNum, ccSec, ccDate, newAddr, orgNo)
        return views.sponsorProfile(request)

    elif userType == 'Admin':
        orgNo = request.POST.get('orgNo')
        db.createSponsor(name, email, password, ccNum, ccSec, ccDate, newAddr, orgNo)
        return views.adminProfile(request)

def createNewAdmin(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = db.getRandomPassword()

    db.createNewAdmin(name, email, password)
    return views.adminProfile(request)