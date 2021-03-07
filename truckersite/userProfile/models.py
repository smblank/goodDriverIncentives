from django.db import models
from django.shortcuts import render
import dbConnectionFunctions


def getNewEmail(request):
    newEmail = request.POST.get('email')
    return updateEmail(newEmail, oldEmail)

def getNewPhone(request):
    newPhone = request.POST.get('phone')

    validPhone = checkPhone(newPhone)

    if validPhone == True:
        return updatePhone(email, newPhone)
    
    else:
        return "Sorry that is not a valid phone number (ex. 555-555-5555)"

def getNewPassword(request):
    newPass = request.POST.get('password1')
    confirmPass = request.POST.get('password2')

    if newPass != confirmPass:
        return "The passwords do not match."
    
    return updatePassword(email, newPass)

