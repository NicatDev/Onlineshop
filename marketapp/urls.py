from django.urls import path,include
from .views import *
from marketapp.jsonresponse import manage_basket,manage_wishlist
urlpatterns = [
    path('',home,name='home'),
    path('mehsullar',shop,name='shop'),
    path('mehsullar/<slug>',shopSingle,name='shopSingle'),
    path('manage_basket/<str:action>/<int:product_id>/', manage_basket, name='manage_basket'),
    path('manage_wishlist/<int:product_id>/', manage_wishlist, name='manage_wishlist'),
]
