from django.shortcuts import render
import dbConnectionFunctions as db

# Create your views here.
def organizationPage(request):
    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    else:
        orgNo = db.getOrgNo(request.session['email'])
        
    result = db.getPointChangeReasons(orgNo)

    class Reason:
        def __init__(self):
            id = -1
            desc = ''

    reasons = []

    for (id, desc) in result:
        tempReason = Reason()
        tempReason.id = id
        tempReason.desc = desc
        reasons.append(tempReason)

    result = db.getSponsors(orgNo)

    class Sponsor:
        def __init__(self):
            id = -1
            name = ''
            email = ''
    
    sponsors = []

    for (id, name, email) in result:
        tempSponsor = Sponsor()
        tempSponsor.id = id
        tempSponsor.name = name
        tempSponsor.email = email
        sponsors.append(tempSponsor)

    result = db.getDrivers(orgNo)

    class Driver:
        def __init__(self):
            id = -1
            name = ''
            email = ''
    
    drivers = []

    for (id, name, email) in result:
        tempDriver = Driver()
        tempDriver.id = id
        tempDriver.name = name
        tempDriver.email = email
        drivers.append(tempDriver)

    imgPath = db.getOrgLogo(orgNo)
    logo = 'http://127.0.0.1:8000/static/img/' + imgPath

    context = {
        'reasons': reasons,
        'sponsors': sponsors,
        'drivers': drivers,
        'logo': logo
    }

    return render(request, 'sponsor_organization.html', context)

def adminOrgs(request):
    result = db.getOrgs()

    class Org:
        def __init__(self):
            id = -1
            name = ''

    orgs = []

    for (orgId, name) in result:
        tempOrg = Org()
        tempOrg.id = orgId
        tempOrg.name = name
        orgs.append(tempOrg)

    if 'adminOrgChoice' in request.session:
        orgNo = request.session['adminOrgChoice']
            
        result = db.getPointChangeReasons(orgNo)

        class Reason:
            def __init__(self):
                id = -1
                desc = ''

        reasons = []

        for (id, desc) in result:
            tempReason = Reason()
            tempReason.id = id
            tempReason.desc = desc
            reasons.append(tempReason)

        result = db.getSponsors(orgNo)

        class Sponsor:
            def __init__(self):
                id = -1
                name = ''
                email = ''
        
        sponsors = []

        for (id, name, email) in result:
            tempSponsor = Sponsor()
            tempSponsor.id = id
            tempSponsor.name = name
            tempSponsor.email = email
            sponsors.append(tempSponsor)

        result = db.getDrivers(orgNo)

        class Driver:
            def __init__(self):
                id = -1
                name = ''
                email = ''
        
        drivers = []

        for (id, name, email) in result:
            tempDriver = Driver()
            tempDriver.id = id
            tempDriver.name = name
            tempDriver.email = email
            drivers.append(tempDriver)

        imgPath = db.getOrgLogo(orgNo)
        logo = 'http://127.0.0.1:8000/static/img/' + imgPath

        context = {
            'reasons': reasons,
            'sponsors': sponsors,
            'drivers': drivers,
            'orgs': orgs,
            'logo': logo
        }
    
    else:
        context = {
            'orgs': orgs
        }

    return render(request, 'admin_organization.html', context)

def getDriverOrgs(request):
    driverId = 1

    result = db.getDriverOrgs(driverID)

    class DriverOrg:
        def __init__(self):
            id = -1
            name = ''
    
    driverOrgs = []

    for (id, name) in result:
        tempOrg = DriverOrg()
        tempOrg.id = id
        tempOrg.name = name
        driverOrgs.append(tempOrg)

    context = {
        'driverOrgs': driverOrgs
    }
        
    return render(request, 'admin_organization.html', context)