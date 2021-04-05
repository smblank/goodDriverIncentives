from django.db import models
import dbConnectionFunctions as db
from dashboard import views as dash
from sponsor import views as spon

# Create your models here.
def setDriverView(request):
    tempEmail = 'temp@email.com'
    orgNo = db.getOrgNo(request.session['email'])
    request.session['tempEmail'] = tempEmail
    request.session['isViewing'] = True

    request.session['tempId'] = db.createTempDriver(tempEmail, orgNo)
    
    return dash.driverDash(request)

def setOriginalView(request):
    db.removeTempDriver(request.session['tempId'])
    del request.session['tempEmail']
    del request.session['tempId']

    request.session['isViewing'] = False

    return spon.sponsorDashDisplay(request)