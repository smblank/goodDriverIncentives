from django.shortcuts import render
import dbConnectionFunctions as db

# Create your views here.
def driverDash(request):
    context = {
        'isSponsor': request.session['isSponsor'],
        'isAdmin': request.session['isAdmin']
    }
    return render(request, "driver_dash.html", context)

def sponsorDash(request):
    context = {
        'isSponsor': request.session['isSponsor'],
        'isAdmin': request.session['isAdmin']
    }
    return render(request, "sponsor_dash.html", context)

def adminDash(request):
    result = db.getAllAdmins()

    class Admin:
        def __init__(self):
            id = -1
            name = ''

    admins = []

    for (id, name, email) in result:
        tempAdmin = Admin()
        tempAdmin.id = id
        tempAdmin.name = name
        admins.append(tempAdmin)

    context = {
        'admins': admins
    }

    return render(request, "admin_dash.html", context)