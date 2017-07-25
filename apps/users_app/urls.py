from django.conf.urls import url
from . import views

urlpatterns = [
    #Home Page
    url(r'^$', views.index),

    #Login & Logout
    url(r'^login$', views.signin),
    url(r'^logout$', views.logout),

    #Register new users
    url(r'^register$', views.create_user),

    #View user profile
    url(r'^user/(?P<user_id>\d+)$', views.user),

]
