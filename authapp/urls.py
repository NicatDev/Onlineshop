from django.urls import path
from authapp.views import register
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('qeydiyyat',register,name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
]