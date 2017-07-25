from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<user_id>\d+)$', views.shoppingCart),
    url(r'^checkout$', views.checkout),
    url(r'^checkout/success$', views.checkout_success),
]