from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.db import models
from marketapp.models import SliderItems,Product,Category,Brand,Color,Size,Order,OrderItem,BlogTag,Blog,Collection,ProductImages,Message,Partner,İnstagramPhoto


class OperatorAdmin(TranslationAdmin):
    pass

class ProductImagesInline(admin.TabularInline):  
    model = ProductImages
    extra = 3  

class ImagesAdmin(TranslationAdmin):
    inlines = [ProductImagesInline]
    
admin.site.register(İnstagramPhoto)
admin.site.register(Product, ImagesAdmin)    
admin.site.register(Category,OperatorAdmin)
admin.site.register(SliderItems,OperatorAdmin)
admin.site.register(Brand,OperatorAdmin)
admin.site.register(Color,OperatorAdmin)
admin.site.register(Size,OperatorAdmin)
admin.site.register(Blog,OperatorAdmin)
admin.site.register(Collection,OperatorAdmin)
admin.site.register(Message)
admin.site.register(BlogTag,OperatorAdmin)
admin.site.register(Partner)

class BookInline(admin.TabularInline): 
    model = OrderItem

class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]

admin.site.register(Order, AuthorAdmin)