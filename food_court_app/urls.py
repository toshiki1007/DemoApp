from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.table_list, name='table_list'),
    url(r'^confirm/(?P<select_table_id>[0-9]+)/$', \
        views.confirm, name='confirm'),
    url(r'^reservation/(?P<select_table_id>[0-9]+)/$',\
        views.reservation, name='reservation'),
    url(r'^order_page/(?P<reservationId>[0-9]+)/$', \
        views.order_page, name='order_page'),
    url(r'^crowd_condition/$', \
        views.crowd_condition, name='crowd_condition')
]