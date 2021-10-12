from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    path('create/', views.create, name='product-create'),
    path('update/<int:pk>', views.update_product, name='product-update'),

    
    #ajax
    path('ajax/load-categories/', views.load_categories, name='ajax-load-categories'),
    path('ajax/delete-image/', views.ajax_delete_image, name='ajax-delete-image'),
    path('ajax/delete-product/', views.ajax_delete_product, name='ajax-delete-product'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)