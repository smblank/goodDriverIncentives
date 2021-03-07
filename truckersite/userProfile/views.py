from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def driverProfile(request):
    return render(request, 'driver_profile.html')

def sponsorProfile(request):
    return render(request, 'sponsor_profile.html')

def adminProfile(request):
    return render(request, 'admin_profile.html')