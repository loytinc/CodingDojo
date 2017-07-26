from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.home, name='home'),
    url(r'^addtocart$', views.addtocart, name='addtocart'),
    url(r'^(?P<id>[0-9]+)/(?P<page>[0-9]+)$', views.category, name='category'),
    url(r'^product/(?P<id>[0-9]+)$', views.product, name='product'),
    url(r'^search/(?P<searchname>[a-zA-Z]+)/(?P<page>[0-9]+)$', views.search, name='search'),
    url(r'^all/(?P<page>[0-9]+)$', views.allprod, name='all'),
    url(r'^edit/(?P<id>[0-9]+)$', views.edit, name='edit'),
    url(r'^delete/(?P<id>[0-9]+)$', views.delete, name='delete'),
    url(r'^edit/(?P<id>[0-9]+)/process$', views.processEdit, name='processEdit'),
]

