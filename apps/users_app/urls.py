from django.conf.urls import url
from . import views

urlpatterns = [
<<<<<<< HEAD
    
]
=======
<<<<<<< HEAD
    #Home Page
    url(r'^$', views.index),
    url(r'^main$', views.index),

    #Login & Logout
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),

    #Register new users
    url(r'^register$', views.create_user),

    #View user profile
    url(r'^user/(?P<user_id>\d+)$', views.user),

]
=======

]
>>>>>>> e93de42686eb4635c0b3b9cb83eed556f283df09
>>>>>>> master
