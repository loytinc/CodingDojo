from django.conf.urls import url
from . import views

urlpatterns = [
    # render routes
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    # url(r'^dashboard/users/(?P<page>[0-9]+)$', views.userdashboard),
    # url(r'^dashboard/admin$', views.dashboard),
    url(r'^dashboard/products$', views.prodDashboard),
    url(r'^dashboard/users$', views.userDashboard),
    url(r'^dashboard/users/(?P<page>[0-9]+)$', views.userDashboardload),
    url(r'^dashboard/products/(?P<page>[0-9]+)$', views.prodDashboardload),
    url(r'^dashboard/products/search/(?P<searchname>[a-zA-Z]+)/(?P<page>[0-9]+)$', views.prodDashboardsearch),
    url(r'^dashboard/products/(?P<id>[0-9\-]+)/(?P<page>[0-9]+)$', views.prodDashboardloadcat),
    url(r'^users/new$', views.add_user),
    url(r'^users/edit$', views.edit_user),
    url(r'^users/delete/(?P<id>\d+)$', views.delete_user),
    url(r'^users/edit/(?P<user_id>\d+)/process$', views.edit_user_admin),
    url(r'^users/show/(?P<user_id>\d+)$', views.profile),
    url(r'^dashboard/admin/remove/(?P<user_id>\d+)$', views.warning),

    # process routes
    url(r'^logoff$', views.logout),
    url(r'^signin/login$', views.login),
    url(r'^register/create$', views.create_user),
    url(r'^users/new/add$', views.admin_create_user),
    url(r'^users/edit/(?P<user_id>\d+)/update_user$', views.update_user),
    url(r'^users/edit/(?P<user_id>\d+)/update_password$', views.update_password),
    url(r'^dashboard/admin/remove/(?P<user_id>\d+)/delete$', views.delete_user),
]
