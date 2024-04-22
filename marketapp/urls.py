from django.urls import path,include
from .views import *
from marketapp.jsonresponse import message,add_wish,add_basket,login_js,delete_order_item
urlpatterns = [
    path('set-language/<lang_code>/<path:url>', set_language, name='set_language'),
    path('set_language_form/', set_language_form, name='set_language_form'),
    

    path('',home,name='home'),
    path('mehsullar',shop,name='shop'),
    path('mehsullar/<slug>',shopSingle,name='shopSingle'),
    path('bloqlar',blogs,name='blogs'),
    path('elaqe',contact,name='contact'),
    path('message',message,name='message'),
    path('bloqlar/<slug>',blogSingle,name='blogSingle'),
    path('add_wish',add_wish,name='add_wish'),
    path('add_basket',add_basket,name='add_basket'),
    path('login_js',login_js,name='login_js'),
    path('delete_order_item',delete_order_item,name='delete_order_item'),
    path('about',about,name='about'),
]
from django.conf.urls import handler500

handler500 = 'marketapp.views.server_error'