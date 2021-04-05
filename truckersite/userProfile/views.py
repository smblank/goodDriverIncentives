from django.shortcuts import render
from django.http import HttpResponse
import dbConnectionFunctions as db

# Create your views here.
def driverProfile(request):
    if (request.session['isViewing']):
        imgPath = db.getProfilePic(request.session['tempEmail'])
    else:
        imgPath = db.getProfilePic(request.session['email'])

    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath

    class Address:
        def __init__(self):
            id = -1
            addr = ''

    addresses = []

    if (request.session['isViewing']):
        result = db.getDriverAddresses(request.session['tempEmail'])
    else:
        result = db.getDriverAddresses(request.session['email'])

    for (id, address) in result:
        newAddr = Address()
        newAddr.addr = address
        newAddr.id = id
        addresses.append(newAddr)
    
    context = {
        'profilePic': profilePic,
        'addresses': addresses
    }
    return render(request, 'driver_profile.html', context)

def sponsorProfile(request):
    if (request.session['isViewing']):
        imgPath = db.getProfilePic(request.session['tempEmail'])
    else:
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