from django.db import models
import dbConnectionFunctions as db
from dashboard import views

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