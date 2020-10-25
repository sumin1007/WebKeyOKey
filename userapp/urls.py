from django.urls import path
from userapp import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('findpassword/', views.findpassword, name='findpassword'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="userapp/password_reset.html"), name='password_reset'),
    path('app/password_reset/done',auth_views.PasswordResetView.as_view(template_name="userapp/password_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="userapp/password_reset_confirm.html"), name='password_reset_confirm'),
    path('app/reset/done',auth_views.PasswordResetView.as_view(template_name="userapp/password_reset_complete.html"), name='password_reset_complete'),
]