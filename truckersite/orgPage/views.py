from django.shortcuts import render
import dbConnectionFunctions as db

# Create your views here.
def organizationPage(request):
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

    context = {
        'reasons': reasons,
        'sponsors': sponsors,
        'drivers': drivers
    }

    return render(request, 'sponsor_organization.html', context)