from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^addquote$', views.addquote),
    url(r'^addtomylist$', views.addtomylist),
    url(r'^remove$', views.remove),
    url(r'^users/(?P<id>\d+)$', views.user),
    url(r'^logout$', views.logout),
]