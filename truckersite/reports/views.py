from django.shortcuts import render
import dbConnectionFunctions as db

def getSponsorContext(request):
    if (request.session['isViewing']):
        imgPath = db.getProfilePic(request.session['email'])
    else: 
        imgPath = db.getProfilePic(request.session['email'])
        
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath

    if (request.session['isViewing']):
        orgNo = db.getOrgNo(request.session['tempEmail'])
    else:
        orgNo = db.getOrgNo(request.session['email'])

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
        'profilePic': profilePic,
        'orgDrivers': drivers
    }
    
    return context

def getInvoiceContext(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath

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
        'profilePic': profilePic,
        'listOrgs': orgs
    }

    return context

# Create your views here.
def sponsorGenerateReport(request):
    context = getSponsorContext(request)
    return render(request, 'sponsor_generate_report.html', context)

def adminGenerateReport(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath
    context = {
        'profilePic': profilePic
    }
    return render(request, 'admin_generate_report.html', context)

def auditLog(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath
    context = {
        'profilePic': profilePic
    }
    return render(request, 'audit_log.html', context)

def invoice(request):
    context = getInvoiceContext(request)
    return render(request, 'invoice.html', context)

def driverSales(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath
    context = {
        'profilePic': profilePic
    }
    return render(request, 'sales_by_driver.html', context)

def sponsorSales(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath

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
        'profilePic': profilePic,
        'orgs': orgs
    }
    return render(request, 'sales_by_sponsor.html', context)