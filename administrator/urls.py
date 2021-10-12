"""albiclick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path

from . import views

urlpatterns = [

   

    path('', views.administrator, name='administrator'),
    path('orders/', views.orders, name='administrator-orders'),
    path('products/', views.products, name='administrator-products'),
    path('users/', views.users, name='administrator-users'),

    path('update-order/<int:pk>',views.update_order , name='administrator-update-order'),


    path('order/<int:pk>',views.order,name='administrator-order'),

    #ajax
    path('ajax/orders/', views.OrderListView.as_view(), name='ajax-administrator-orders'),
    path('ajax/products/', views.ProductListView.as_view(), name='ajax-administrator-products'),
    path('ajax/users/', views.UsersListView.as_view(), name='ajax-administrator-users'),
    
    #path('ajax/load-categories/', views.ajax_load_categories, name='ajax-load-categories-menu'),

    #shipments
    path('shipments/',views.ShipmentsListView.as_view(),name='administrator-shipments'),
    path('shipments/create',views.create_shipment,name='administrator-shipments-create'),
    path('shipments/update/<int:pk>',views.update_shipment,name='administrator-shipments-update'),
    path('ajax/shipments/delete',views.ajax_delete_shipment,name='ajax-administrator-shipments-delete'),


]