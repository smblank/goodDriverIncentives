from django.shortcuts import render
from django.http import HttpResponse
import dbConnectionFunctions as db

# Create your views here.
def driverProfile(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath
    context = {
        'profilePic': profilePic
    }
    return render(request, 'driver_profile.html', context)

def sponsorProfile(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath
    context = {
        'profilePic': profilePic
    }
    return render(request, 'sponsor_profile.html', context)

def adminProfile(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath
    context = {
        'profilePic': profilePic
    }
    return render(request, 'admin_profile.html', context)