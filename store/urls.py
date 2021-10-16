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


    path('terms', views.terms, name='terms'),
    path('policies', views.policies, name='policies'),


    path('', views.index.as_view(), name='index'),
    path('product/<int:pk>/', views.product_view, name='product'),

    path('see-products/', views.product_list_base, name='see-products'),

    path('see-products/<category>/', views.product_list_base, name='see-products-args'),
    
    path('see-products/destaques/', views.product_list_destaques, name='see-products-destaques'),
    


    path('ajax/see-products/', views.ProductListView.as_view(), name='ajax-see-products'),

    #ajax

    path('ajax/load-categories/', views.ajax_load_categories, name='ajax-load-categories-menu'),


    path('ajax/add-cart/<int:pk>/', views.ajax_add_cart, name='ajax-add-cart'),
    
    path('ajax/remove-item-cart/<int:pk>/', views.ajax_remove_item_cart, name='ajax-remove-item-cart'),

    path('ajax/update-qty-cart/<int:pk>/<type>/',views.ajax_update_qty_cart, name='ajax-update-qty-cart'),
    path('ajax/cleancart/',views.ajax_clean_cart, name='ajax-clean-cart'),
    path('ajax/get-cart/',views.ajax_get_cart, name='ajax-get-cart'),
    
]
