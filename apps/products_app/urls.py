from django.conf.urls import url
from . import views

<<<<<<< HEAD
urlpatterns = [
    
]
=======
urlpatterns=[
    url(r'^$', views.home, name='home'),
    url(r'^(?P<id>[0-9]+)/(?P<page>[0-9]+)$', views.category, name='category'),
    url(r'^products/(?P<id>[0-9]+)$', views.product, name='product'),
    url(r'^search/(?P<searchname>[a-zA-Z]+)/(?P<page>[0-9]+)$', views.search, name='search'),
]

>>>>>>> f1c5b1383cf57d64527c66f4b1a73db850bd996d
