from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register, name='register'),
    url(r'^authenticate$', views.authenticate, name='authenticate'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^quote', views.quotehome, name='quotehome'),
    url(r'^addquote$', views.addquote, name='addquote'),
    url(r'^user/(?P<id>\d+)$', views.user, name='user'),
    url(r'^favorites$', views.favorite, name='favorite'),
    url(r'^remove$', views.remove, name='remove')
]
