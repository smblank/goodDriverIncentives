from django.shortcuts import render

# Create your views here.
def driverDash(request):
    return render(request, "driver_dash.html")

def sponsorDash(request):
    return render(request, "sponsor_dash.html")

def adminDash(request):
    return render(request, "admin_dash.html")