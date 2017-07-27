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
    url(r'^orders/(?P<order_id>\d+)$', views.view_order),
    url(r'^orders/page/(?P<page_num>\d+)$', views.page_process),
    url(r'^orders/search/(?P<searchname>[a-zA-Z]+)/(?P<page_num>[0-9]+)$', views.search_process),
    url(r'^orders/status/(?P<status>[a-zA-Z]+)/(?P<page>[0-9]+)$', views.status_process),
    url(r'^(?P<id>[0-9]+)/changestatus/(?P<status>[a-zA-Z]+)$', views.changestatus),

]