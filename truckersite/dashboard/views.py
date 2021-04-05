from django.shortcuts import render

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
    return render(request, "admin_dash.html")