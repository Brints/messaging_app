from django.urls import path

from apps.authentication import views

app_name = 'authentication'
urlpatterns = [
    path('register/', views.create_user_and_get_tokens, name='register'),
    path('login/', views.login_user_and_get_tokens, name='login'),
    path('generate-password/', views.generate_strong_password, name='generate_password'),
]