from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.table_list, name='table_list'),
    url(r'^confirm/(?P<select_table_id>[0-9]+)/$', \
        views.confirm, name='confirm'),
    url(r'^reservation/(?P<select_table_id>[0-9]+)/$',\
        views.reservation, name='reservation'),
    url(r'^select_store_for_order/(?P<reservation_id>[0-9]+)/$', \
        views.select_store_for_order, name='select_store_for_order'),
    url(r'^order_page/$', \
        views.order_page, name='order_page'),
    url(r'^order_page_all_store/(?P<reservation_id>[0-9]+)/$', \
        views.order_page_all_store, name='order_page_all_store'),
    url(r'^crowd_condition/$', \
        views.crowd_condition, name='crowd_condition'),
    url(r'^add_store_view/$', \
        views.add_store_view, name='add_store_view'),
    url(r'^add_store/$', \
        views.add_store, name='add_store'),
    url(r'^order/$', \
        views.order, name='order'),
    url(r'^order_confirm/$', \
        views.order_confirm, name='order_confirm'),
    url(r'^manage_order_view/$', \
        views.manage_order_view, name='manage_order_view'),
    url(r'^select_store/$', \
        views.select_store, name='select_store'),
    url(r'^order_supply/$', \
        views.order_supply, name='order_supply'),
    url(r'^order_cancel/$', \
        views.order_cancel, name='order_cancel'),
    url(r'^order_page_all_store/(?P<reservation_id>[0-9]+)/menu_detail', \
        views.menu_detail, name='menu_detail'),
]
