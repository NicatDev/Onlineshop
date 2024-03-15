from django.contrib import admin

from django.db import models
from marketapp.models import Product,Category,Brand,Color,Size,Order,OrderItem,BlogTag,Blog,Collection,ProductImages,Message,Partner,İnstagramPhoto

# class MyModelAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.TextField: {'widget': CKEditorWidget(config_name='default')},
#     }
#     # exclude = ('content_without_ck','content','name','bottomcontent','sidename','sidecontent','bottomname')
class ProductImagesInline(admin.TabularInline):  # or use admin.StackedInline for a stacked layout
    model = ProductImages
    extra = 3  # number of empty forms to display

class ImagesAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline]
admin.site.register(İnstagramPhoto)
admin.site.register(Product, ImagesAdmin)    
    
admin.site.register(Category)

admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Size)

admin.site.register(Blog)

admin.site.register(Collection)
admin.site.register(Message)
admin.site.register(BlogTag)
admin.site.register(Partner)
# admin.site.register(Training)
# admin.site.register(Team)
class BookInline(admin.TabularInline):  # veya StackedInline
    model = OrderItem

class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]

admin.site.register(Order, AuthorAdmin)