from django.urls import path
from django.contrib.auth import views as auth_views
from custom_auth import views

app_name = "custom_auth"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="custom_auth/login.html"), name="login"),
    path("verify-login/", views.verify_login, name="verify_login"),
    path("logout/", views.custom_logout, name="logout"),
    path('register/', views.register, name='register'),
    path("verify-email/", views.verify_email, name="verify_email"),
]

