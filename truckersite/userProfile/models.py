from django.db import models
from django.shortcuts import render
import dbConnectionFunctions as db
from userProfile import views

email = 'johndoe@email.com'
oldEmail = email

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
    response = db.updateEmail(newEmail, oldEmail)
    return render(request, 'driver_profile.html')

def getNewDriverPhone(request):
    newPhone = request.POST.get('phone')

    validPhone = checkPhone(newPhone)

    if validPhone == True:
        newPhone = formatPhone(newPhone)
        response = db.updatePhone(email, newPhone)
    
    else:
        response = "Sorry that is not a valid phone number (ex. 555-555-5555)"

    return render(request, 'driver_profile.html')

def getNewDriverPassword(request):
    newPass = request.POST.get('password1')
    confirmPass = request.POST.get('password2')

    if newPass != confirmPass:
        response = "The passwords do not match."
        return render(request, 'driver_profile.html')
    
    response = db.changePassword(email, newPass)

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

    response = db.addAddress(email, newAddr)

    return views.driverProfile(request)

def getDriverDefaultAddr(request):
    defaultAddr = request.POST.get('default')

    response = db.setDefaultAddress(email, defaultAddr)

    return views.driverProfile(request)

def getDriverProfilePic(request):
    profilePic = request.POST.get('profilePic')

    response = db.setProfilePic(email, profilePic)

    return views.driverProfile(request)
