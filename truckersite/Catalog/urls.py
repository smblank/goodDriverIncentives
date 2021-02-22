from Catalog import views
from django.conf.urls import url

app = 'Catalog'

urlpatterns = [
    url(r'^driver_catalog/$', views.Catalog, name='Catalog')
]

