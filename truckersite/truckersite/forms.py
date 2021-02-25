from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from mysql.connector import connect
from django.contrib import messages
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required

def getDB():
    try:
        connection = connect(host = 'truckingdb.c9tkxb1tjvpp.us-east-1.rds.amazonaws.com', user = 'admin', password = 'accesstodb', database = 'DRIVER_DB', autocommit = True)
    
    except Error as err:
        print(err)

    else:
        return connection

def getCursor(connection):
    try:
        cursor = connection.cursor(buffered = True)
    
    except Error as err:
        print(err)
    
    else:
        return cursor

def getUserType(connection, cursor, email):
    try:
        query = "SELECT getUserType(%s)"

        cursor.execute(query, (email,))
        result = cursor.fetchone()

        for userType in result:
            return userType
    
    except Error as err:
        print(err)

#need to move this to index @app.route('/index/', methods=['GET', 'POST'])
def loginpg(request):
    connection = getDB()
    cursor = getCursor(connection)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        #might need to fix below
        cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor1.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password,))
        account = cursor1.fetchone()
        user= authenticate(request, account['email'], account['password'])

        if account & user is not None:
            login(request,user)
            request.session['loggedin'] = True
            request.session['id'] = account['UserID']
            request.session['email'] = account['email']
            request.session['role'] = getUserType( connection,cursor,account['email'])
            


            return moveout()
        else:
            messages.info(request, 'Incorrect login')
    context={}
    return render(request, '/index.html/', context)


#need to check vs role 
def moveout():
    if 'loggedin' in session:
        if request.session.get('role') == Driver
            return redirect('/driver_dash.html/')
        if request.session.get('role') == Sponsor
            return redirect('/sponsor_dash.html/')
        if request.session.get('role') == Admin
            return redirect('/admin_dash.html/')
    return redirect('/index/')

