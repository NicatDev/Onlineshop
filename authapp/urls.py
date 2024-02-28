from django.urls import path
from authapp.views import register,login_view,logout_view,shopping,wish
urlpatterns = [
    path('qeydiyyat',register,name='register'),
    path('giris',login_view,name='login'),
    path('shopping',shopping,name='shopping'),
    path('wish',wish,name="wish"),
    path('logout/', logout_view, name='logout'),
]