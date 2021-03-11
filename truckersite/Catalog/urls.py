from Catalog import views
from django.conf.urls import url

app = 'Catalog'

urlpatterns = [
    url(r'^driver_catalog/$', views.product_list, name='Catalog'),
    url(r'^driver_cart/(?P<slug>[\w-]+)/$', views.add_to_cart, name='addToCart'),
    url(r'^driver_cart/(?P<slug>[\w-]+)/$', views.remove_from_cart, name='removeFromCart'),
]

