from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls import url

urlpatterns = [
    path('', store_v, name='store'),
    path('cart/', cart_v, name='cart'),
    path('checkout/', checkout_v, name='checkout'),
    path('update_item/', updateItem_v, name='update_item'),
    path('process_order/', processOrder_v, name='process_order'),
    # path('notify/', notify_handler, name='payfast_notify'),
    # path('detail/<str:pk>', detail_v, name='detail_v'),
]
