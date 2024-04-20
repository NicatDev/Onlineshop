from django.db import models
from marketapp.utils import *
from datetime import datetime
from django.utils.text import slugify
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseMixin(models.Model):
    slug = models.SlugField(unique=True,editable=False,blank=True,null=True)
    created_at = models.DateField(auto_now=True,blank=True,null=True,)
    
    class Meta:
        abstract = True


class MetaMixin(models.Model):
    seo_title = models.CharField(max_length=1200,null=True,blank=True,verbose_name='title for seo')
    seo_keyword = models.CharField(max_length=1200,null=True,blank=True,verbose_name='keyword for seo')
    seo_alt = models.CharField(max_length=1200,null=True,blank=True)
    seo_description = models.CharField(max_length=1200,null=True,blank=True,verbose_name='description for seo')
        
    class Meta:
        abstract = True

from colorfield.fields import ColorField

class Color(BaseMixin):
    color = ColorField()
    name = models.CharField(max_length=200)
    dark = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = get_slug(self.name)
        
        if Color.objects.filter(slug=new_slug).exists():
            count = 0
            while Color.objects.filter(slug=new_slug).exists():
                new_slug = f"{get_slug(self.name)}-{count}"
                count += 1
        self.slug = new_slug
        super(Color, self).save(*args, **kwargs)
   
class Size(BaseMixin):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name  
    
    def save(self, *args, **kwargs):
        new_slug = get_slug(self.name)
        
        if Size.objects.filter(slug=new_slug).exists():
            count = 0
            while Size.objects.filter(slug=new_slug).exists():
                new_slug = f"{get_slug(self.name)}-{count}"
                count += 1
        self.slug = new_slug
        super(Size, self).save(*args, **kwargs)       
    
class Brand(BaseMixin):
    name = models.CharField(max_length = 200)
       
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        new_slug = get_slug(self.name)
        
        if Brand.objects.filter(slug=new_slug).exists():
            count = 0
            while Brand.objects.filter(slug=new_slug).exists():
                new_slug = f"{get_slug(self.name)}-{count}"
                count += 1
        self.slug = new_slug
        super(Brand, self).save(*args, **kwargs)
    
class Category(MetaMixin,BaseMixin):
    name = models.CharField(max_length = 200)
    image = models.ImageField(null=True,blank=True)
    in_slide = models.BooleanField(default = False)
    
    def __str__(self):
        return self.name + '--'

    def save(self, *args, **kwargs):
        new_slug = get_slug(self.name)
        
        if Category.objects.filter(slug=new_slug).exists():
            count = 0
            while Category.objects.filter(slug=new_slug).exists():
                new_slug = f"{get_slug(self.name)}-{count}"
                count += 1
        self.slug = new_slug
        super(Category, self).save(*args, **kwargs)
    
class SliderItems(models.Model):
    name = models.CharField(max_length = 200)
    image = models.ImageField()
    feature = models.CharField(max_length = 200,null=True,blank=True)
    in_slide = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Collection(MetaMixin,BaseMixin):
    name = models.CharField(max_length = 200)
    image = models.ImageField()
    feature = models.CharField(max_length = 200,null=True,blank=True)
    in_slide = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        new_slug = get_slug(self.name)
        
        if Collection.objects.filter(slug=new_slug).exists():
            count = 0
            while Collection.objects.filter(slug=new_slug).exists():
                new_slug = f"{get_slug(self.name)}-{count}"
                count += 1
        self.slug = new_slug
        super(Collection, self).save(*args, **kwargs)


class Product(MetaMixin,BaseMixin):
    name = models.CharField(max_length = 200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.SmallIntegerField(default=0)
    description = models.TextField(null=True,blank=True)
    stock = models.BooleanField(default=True)
    color = models.ManyToManyField(Color,blank=True)
    size = models.ManyToManyField(Size,blank=True)
    collection = models.ManyToManyField(Collection,blank=True)
    category = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand,null=True,blank=True,on_delete=models.SET_NULL)
    new = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    most_searched = models.BooleanField(default=False)
    wishlist = models.ManyToManyField(User,blank=True,related_name='wishproducts')
    material = models.CharField(max_length = 200,null=True,blank=True)
    product_code = models.CharField(max_length = 300,null=True,blank=True)

    def __str__(self):
        return  self.name + '--'

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = get_slug(self.name)
            if Product.objects.filter(slug=new_slug).exists():
                count = 0
                while Product.objects.filter(slug=new_slug).exists():
                    new_slug = f"{get_slug(self.name)}-{count}"
                    count += 1
            self.slug = new_slug
        super(Product, self).save(*args, **kwargs)
    
    def get_main_image(self):
        main_image = self.images.first()
        return main_image.image if main_image else None
    
    def get_discount_price(self):
        if self.discount_percent>0:
            discounted = self.price * (100-self.discount_percent) /100
        else:
            discounted = self.price
        return discounted
    
    def get_absolute_url(self):
        return reverse('shopSingle', kwargs={'slug': self.slug})
        
class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField()
    
    def __str__(self):
        return f'{self.product.name}-{self.pk}'
    
    
class Order(models.Model):
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='myproducts')
    phone_number = models.CharField(max_length=200,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    

    def __str__(self):
        return  f'{self.status}-{self.id}'
    

    
class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,related_name='orderitems',blank=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True,blank=True)
    size = models.ForeignKey(Size,on_delete=models.CASCADE,null=True,blank=True)
        
    def __str__(self):
        return f'{self.product.name} ' 
    
    

class BlogTag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Blog(BaseMixin,MetaMixin):
    tag = models.ForeignKey(BlogTag,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    content_without_ck = models.CharField(max_length=200)
    content2 = models.TextField()
    image = models.ImageField()
    
    def __str__(self):
        return self.title

    class META:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = get_slug(self.title)
            
            if Blog.objects.filter(slug=new_slug).exists():
                count = 0
                while Blog.objects.filter(slug=new_slug).exists():
                    new_slug = f"{get_slug(self.title)}-{count}"
                    count += 1
            self.slug = new_slug
        super(Blog, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blogSingle', kwargs={'slug': self.slug})
    
class Message(models.Model):
    name = models.CharField(max_length = 200)
    phone = models.CharField(max_length = 200)
    subject = models.CharField(max_length = 200)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email
    

class Partner(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length = 200 )
    href = models.CharField(max_length = 200,null=True,blank=True)
    
    def __str__(self):
        return self.title
    
    
class İnstagramPhoto(models.Model):
    image = models.ImageField()
    href = models.CharField(max_length=500)
    
    def __str__(self):
        return self.href
    
# class Services(BaseMixin):
#     name = models.CharField(max_length = 800)
#     description = models.TextField()
#     description_without_ck = models.CharField(max_length = 200)
#     icon = models.ImageField(null=True,blank=True)
#     image = models.ImageField(null=True,blank=True)
#     bottomdescription = models.TextField()
#     ordering = models.SmallIntegerField(null=True,blank=True)
    
#     def __str__(self):
#         return self.name
    
#     def save(self, *args, **kwargs):
#         new_slug = seo(self.name)
#         self.slug = new_slug
#         if Services.objects.filter(slug=new_slug).exists():
#             count = 0
#             while Services.objects.filter(slug=new_slug).exists():
#                 new_slug = f"{seo(self.name)}-{count}"
#                 count += 1
#         super(Services, self).save(*args, **kwargs)
        
#     def get_absolute_url(self):
#         return reverse('serviceSingle', kwargs={"slug": self.slug})