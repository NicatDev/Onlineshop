from django.urls import path
from authapp.views import register,login_view,logout_view,shopping,wish,order,confirm
urlpatterns = [
    path('qeydiyyat',register,name='register'),
    path('tesdiq/<username>/<code>',confirm,name='confirm'),
    path('giris',login_view,name='login'),
    path('shopping/<form_name>',shopping,name='shopping'),
    path('shopping',shopping,name='shopping'),
    path('wish',wish,name="wish"),
    path('logout/', logout_view, name='logout'),
    path('order/', order, name='order'),
]