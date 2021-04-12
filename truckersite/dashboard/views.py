from django.shortcuts import render
import dbConnectionFunctions as db

# Create your views here.
def driverDash(request):
    if (request.session['isViewing']):
        driverID = db.getUserID(request.session['tempEmail'])
    else:
        driverID = db.getUserID(request.session['email'])
    
    result = db.getDriverOrgs(driverID)

    class Org:
        def __init__(self):
            id = -1
            name = ''
        
    orgs = []

    for (id, name) in result:
        tempOrg = Org()
        tempOrg.id = id
        tempOrg.name = name
        orgs.append(tempOrg)

    if (request.session['isViewing']):
        email = request.session['tempEmail']
        org = db.getOrgNo(request.session['email'])
    else:
        email = request.session['email']
        org = request.session['orgID']
    
    points = db.getDriverPoints(email, org)

    context = {
        'isSponsor': request.session['isSponsor'],
        'isAdmin': request.session['isAdmin'],
        'driverOrgs': orgs,
        'points': points
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

    result = db.getOrgs()

    class Org:
        def __init__(self):
            id = -1
            name = ''
        
    orgs = []

    for (id, name) in result:
        tempOrg = Org()
        tempOrg.id = id
        tempOrg.name = name
        orgs.append(tempOrg)

    context = {
        'admins': admins,
        'orgs': orgs
    }

    return render(request, "admin_dash.html", context)