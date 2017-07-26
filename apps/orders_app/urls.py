from django.conf.urls import url
from . import views

urlpatterns = [
    # shopping cart
    url(r'^$', views.shoppingCart),
    url(r'^checkout$', views.checkout),
    url(r'^checkout/success$', views.checkout_success),

    # order tracker
    url(r'^orders$', views.track_orders),
    url(r'^orders/status_update$', views.update_status),
    url(r'^orders/(?P<order_id>\d+)$', views.update_status),

]