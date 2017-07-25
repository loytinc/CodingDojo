from django.conf.urls import url
from . import views

urlpatterns = [
    # Home page
    url(r'^$', views.index),
    url(r'^main$', views.index),

    url(r'^login$', views.signin),
    url(r'^register$', views.create_user),
    url(r'^logout$', views.logout),

    # User Profile information
    url(r'^user/(?P<user_id>\d+)$', views.user),

]
