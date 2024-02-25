from django.urls import path,include
from .views import *
from marketapp.jsonresponse import message
urlpatterns = [
    path('',home,name='home'),
    path('mehsullar',shop,name='shop'),
    path('mehsullar/<slug>',shopSingle,name='shopSingle'),
    path('bloqlar',blogs,name='blogs'),
    path('elaqe',contact,name='contact'),
    path('message',message,name='message'),
    path('bloqlar/<slug>',blogSingle,name='blogSingle')
]
