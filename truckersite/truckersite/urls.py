"""truckersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from truckersite import views, forms
from userProfile import views as profileViews
from userProfile import models as profileOps

urlpatterns = [
    path('',forms.loginpg, name = "login"), 
    path('getNewDriverEmail', profileOps.getNewDriverEmail, name = "getNewDriverEmail"),
    path('getNewDriverPass', profileOps.getNewDriverPassword, name = 'getNewDriverPass'),
    path('getNewDriverPhone', profileOps.getNewDriverPhone, name = 'getNewDriverPhone'),
    path('getNewDriverAddress', profileOps.getNewDriverAddress, name = 'getNewDriverAddress'),
    path('getDriverDefaultAddr', profileOps.getDriverDefaultAddr, name = 'getDriverDefaultAddr'),
    path('getNewDriverProfilePic', profileOps.getDriverProfilePic, name = 'getNewDriverProfilePic'),
    path('driverProfile/', profileViews.driverProfile, name = "driverProfile"),
    path('admin/', admin.site.urls),
    url(r'^driver_catalog', include('Catalog.urls')),
    path('',views.userreggin),

