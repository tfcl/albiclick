from django.conf.urls import include, url
from django.forms.forms import Form
from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from django.views.generic import edit
from users.forms import UserLoginForm, ChandPasswordForm
from .views import login_view,logout_view,register,dashboard,ajax_my_orders,ajax_account,ajax_edit_account,ajax_adresses,edit_adress
urlpatterns = [
  
    url('login/',login_view, name='login'),
    url('logout/',logout_view, name='logout'),
    
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html', form_class =ChandPasswordForm),
    ),

    url('register/',register,name='register'),

    path('dashboard/<int:x>',dashboard,name="dashboard-args"),
    url('dashboard/',dashboard,name="dashboard"),

    url(r"^accounts/", include("django.contrib.auth.urls")),

    #ajax

    path('ajax/account/', ajax_account, name='ajax-get-account'),
    path('ajax/my-orders/', ajax_my_orders, name='ajax-get-my-orders'),
    path('ajax/my-adresses/',ajax_adresses, name='ajax-get-my-adresses'),
    path('ajax/edit-account/', ajax_edit_account, name='ajax-edit-account'),
    #edit

    path('edit-adress/', edit_adress, name=''),
    path('edit-adress/<int:pk>/', edit_adress, name='edit-adress-args'),
    re_path(r'^edit-adress/(?P<type>billing|normal)', edit_adress, name='edit-adress'),

]

