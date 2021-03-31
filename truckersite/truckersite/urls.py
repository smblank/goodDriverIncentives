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
from Catalog.views import sponsor_catalog
from Catalog.views import product_list
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from truckersite import views, forms

from userProfile import views as profileViews
from userProfile import models as profileOps

from reports import views as reportViews
from reports import models as reportOps

from sponsor import views as sponsorViews
from sponsor import models as sponsorOps

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',forms.login), 
    path('login', forms.loginpg, name = 'login'),
    
    path('reg',views.userreggin, name = 'reg'),

    #Driver profile forms
    path('getNewDriverEmail', profileOps.getNewDriverEmail, name = "getNewDriverEmail"),
    path('getNewDriverPass', profileOps.getNewDriverPassword, name = 'getNewDriverPass'),
    path('getNewDriverPhone', profileOps.getNewDriverPhone, name = 'getNewDriverPhone'),
    path('getNewDriverAddress', profileOps.getNewDriverAddress, name = 'getNewDriverAddress'),
    path('getDriverDefaultAddr', profileOps.getDriverDefaultAddr, name = 'getDriverDefaultAddr'),
    path('getNewDriverProfilePic', profileOps.getDriverProfilePic, name = 'getNewDriverProfilePic'),
    path('driverProfile', profileViews.driverProfile, name = "driverProfile"),

    #Sponsor profile forms
    path('getNewSponsorProfilePic', profileOps.getSponsorProfilePic, name = 'getNewSponsorProfilePic'),
    path('getNewSponsorEmail', profileOps.getNewSponsorEmail, name = 'getNewSponsorEmail'),
    path('getNewDriverPass', profileOps.getNewSponsorPassword, name = 'getNewDriverPass'),
    path('getNewDriverPhone', profileOps.getNewSponsorPhone, name = 'getNewDriverPhone'),
    path('sponsorProfile/', profileViews.sponsorProfile, name = 'sponsorProfile'),

    #Admin profile forms
    path('getNewAdminProfilePic', profileOps.getAdminProfilePic, name = 'getNewAdminProfilePic'),
    path('getNewAdminEmail', profileOps.getNewAdminEmail, name = 'getNewAdminEmail'),
    path('getNewAdminPass', profileOps. getNewAdminPassword, name = 'getNewAdminPass'),
    path('adminProfile/', profileViews.adminProfile, name = 'adminProfile'),

    #Sponsor report generation
    path('sponsorReportGeneration/', reportViews.sponsorGenerateReport, name = 'sponsorReportGeneration'),
    path('getSponsorReport', reportOps.getSponsorReport, name = 'getSponsorReport'),

    #Admin report generation
    path('adminReportGeneration/', reportViews.adminGenerateReport, name = 'adminReportGeneration'),
    path('auditLog/', reportViews.auditLog, name = 'auditLog'),
    path('invoice/', reportViews.invoice, name = 'invoice'),
    path('driverSales/', reportViews.driverSales, name = 'driverSales'),
    path('sponsorSales/', reportViews.sponsorSales, name = 'sponsorSales'),
    path('getAuditLog', reportOps.getAuditLog, name = 'getAuditLog'),
    path('getInvoice', reportOps.getInvoice, name = 'getInvoice'),
    path('getDriverSales', reportOps.getDriverSales, name = 'getDriverSales'),
    path('getSponsorSales', reportOps.getSponsorSales, name = 'getSponsorSales'),

    path('driver_catalog/', product_list, name='catalog'),
    path('sponsor_catalog/', sponsor_catalog, name='catalog'),
    path('admin/', admin.site.urls),

    #Sponsor
    path('sponsor_dash/', sponsorViews.sponsorDashDisplay, name = 'sponsorDashDisplay'),
    path('application/<int:applicant_id>', sponsorViews.sponsorViewApplicant, name = 'sponsorViewApplicant'),
    path('accept_applicant/<int:applicant_id>', sponsorViews.sponsorAcceptApplicant, name = 'sponsorAcceptApplicant'),
    path('reject_applicant/<int:applicant_id>', sponsorViews.sponsorRejectApplicant, name = 'sponsorRejectApplicant'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)