from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.table_list, name='table_list'),
    url(r'^confirm/(?P<select_tableId>[0-9]+)/$', views.confirm, name='confirm'),
    url(r'^reservation/(?P<select_tableId>[0-9]+)/$', views.reservation, name='reservation')
]