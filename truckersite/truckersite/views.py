from django.shortcuts import render
from truckersite.models import Uregister
from django.contrib import messages

#add reguser to settings
def userreggin(request):
    if request.method=='POST':
        if request.get('Name') and request.get('lname') and request.get('PhoneNo') and request.get('Email') and request.get('Address') and request.get('address2') and request.get('city') and request.get('state') and request.get('zipcode') and request.get('org') and request.get('sponsor'):
            saverecord= Uregister()
            saverecord.Name = request.get('Name')
            saverecord.lname = request.get('lname')
            saverecord.PhoneNo = request.get('PhoneNo')
            saverecord.Email = request.get('Email')
            saverecord.Address = request.get('Address')
            saverecord.address2 = request.get('address2')
            saverecord.city = request.get('city')
            saverecord.state = request.get('state')
            saverecord.zipcode = request.get('zipcode')
            saverecord.org = request.get('org')
            saverecord.sponsor = request.get('sponsor')
            saverecord.save()
            messages.success(request,"Registration completed")
            return render(request,'index.html')
    else:
        return render(request,'apply.html')