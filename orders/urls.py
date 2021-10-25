from orders.views import checkout
from django.contrib.auth import views
from django.urls import path,re_path
from . import views
urlpatterns = [

    path('checkout/', views.checkout, name='checkout'),
    path('checkout/payment', views.payment, name='checkout-payment'),
    path('<int:pk>/', views.order_details, name='order-details'),
    


    #payments ajax
    path('ajax/payment/mb', views.ajax_payment_mb, name='checkout-payment-mb'),
    path('ajax/payment/mbway', views.ajax_payment_mbway, name='checkout-payment-mbway'),
    path('ajax/payment/credit', views.ajax_payment_credit, name='checkout-payment-credit'),
    path('ajax/payment/payshop', views.ajax_payment_payshop, name='checkout-payment-payshop'),


    path('ajax/payment/get_total', views.ajax_get_total, name='checkout-payment-get-total'),
    path('ajax/get_unread', views.ajax_get_unread, name='ajax-get-unread'),

    path('ajax/cupons/verify',views.ajax_check_cupon,name='orders-cupons-check'),

]
