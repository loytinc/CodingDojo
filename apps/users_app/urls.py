from django.conf.urls import url
from . import views

urlpatterns = [
<<<<<<< HEAD
    #Home Page
    url(r'^$', views.index),

    #Login & Logout
    url(r'^login$', views.signin),
    url(r'^logout$', views.logout),

    #Register new users
    url(r'^register$', views.create_user),

    #View user profile
=======
    # Home page
    url(r'^$', views.index),
    url(r'^main$', views.index),

    url(r'^login$', views.signin),
    url(r'^register$', views.create_user),
    url(r'^logout$', views.logout),

    # User Profile information
>>>>>>> master
    url(r'^user/(?P<user_id>\d+)$', views.user),

]
