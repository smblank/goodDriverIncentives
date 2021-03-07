from Catalog import views
from django.conf.urls import url

app = 'Catalog'

urlpatterns = [
    url(r'^driver_catalog/$', views.Catalog, name='Catalog'),
    url(r'^driver_cart/(?P<slug>[\w-]+)/$', views.addToCart, name='addToCart'),
    url(r'^driver_cart/(?P<slug>[\w-]+)/$', views.removeFromCart, name='removeFromCart'),
]

