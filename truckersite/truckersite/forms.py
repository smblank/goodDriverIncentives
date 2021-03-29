from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
import dbConnectionFunctions as db

def login(request):
    return render(request, 'index.html')

#need to move this to index @app.route('/index/', methods=['GET', 'POST'])
def loginpg(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        correctPassword = db.checkPassword(email, password)

        if correctPassword == True:
            request.session['loggedin'] = True
            request.session['id'] = db.getUserID(email)
            request.session['email'] = email
            request.session['role'] = db.getUserType(email)


            
            return moveout(request)
        else:
            messages.success(request, 'Incorrect Email or Password')
            return render(request, 'index.html')

def logoutpg(request):

    del request.session['loggedin']
    del request.session['id']
    del request.session['email']
    del request.session['role']
    
    return render(request, 'index.html')

#need to check vs role 
def moveout(request):
    if 'loggedin' in request.session:
        print(request.session.get('role'))
        if request.session.get('role') == 'Driver':
            return render(request, 'driver_dash.html')
        if request.session.get('role') == 'Sponsor':
            return render(request, 'sponsor_dash.html')
        if request.session.get('role') == 'Admin':
            return render(request, 'admin_dash.html')
    else:
        print('not logged in...displaying login')
        return render(request, 'index.html')

