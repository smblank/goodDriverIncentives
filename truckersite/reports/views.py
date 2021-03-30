from django.shortcuts import render
import dbConnectionFunctions as db

# Create your views here.
def sponsorGenerateReport(request):
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath
    context = {
        'profilePic': profilePic
    }
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
    imgPath = db.getProfilePic(request.session['email'])
    profilePic = 'http://127.0.0.1:8000/static/img/' + imgPath
    context = {
        'profilePic': profilePic
    }
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
    context = {
        'profilePic': profilePic
    }
    return render(request, 'sales_by_sponsor.html', context)