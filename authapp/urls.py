from django.urls import path
from authapp.views import register

urlpatterns = [
    path('qeydiyyat',register,name='register'),
]