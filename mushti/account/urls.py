
from django.urls import path
from .views import *
from account.views import password_reset_request
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/',user_create_view,name='signup_view'),
    path('logout/',logout_view,name="logout_view"),
    path('profile/', profile_detail_view, name= 'detail_view'),
    path('profile/create',profile_create_view,name='create_view'),
    path('login/',login_view,name="login_view"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset/reset_done.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/change_password.html"),
        name="password_reset_confirm"),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/reset_complete.html"),
        name="password_reset_complete"),
    path('password/reset/', password_reset_request, name='password_request')
    
]