from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from marketapp.models import *
from django.urls import translate_url
from django.db.models import Q,F,FloatField,Count
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count
from django.conf import settings

# from marketapp.forms import Messageform

# def home(request):
#     portfolio_categories = Portfolio_category.objects.all()
#     portfolio = Portfolio.objects.all().select_related('category')
#     services = Services.objects.all().order_by('ordering')
#     if len(services)>6:
#         services = services[0:6]
#     blogs = Blog.objects.all().select_related('category').only('category','category__name','title','content_without_ck','mainimage','backimage')
#     if len(blogs)>3:
#         blogs = blogs[0:3]
#     partners = Partners.objects.all()
#     faq = Faq.objects.all()
#     trainings = Training.objects.all()
#     if len(trainings)>3:
#         trainings = trainings[0:3]
#     context = {
#         'trainings':trainings,
#         'partners':partners,
#         'faq':faq,
#         'blogs':blogs,
#         'portfolio':portfolio,
#         'services':services,
#         'portfolio_categories':portfolio_categories
#     }
#     return render(request,'home.html',context)

def home(request):
    products = Product.objects.all().order_by('-created_at')[0:6]
    best_seller = Product.objects.filter(best_seller=True)[:6]
    most_searched = Product.objects.filter(most_searched=True)[:6]
    new = Product.objects.filter(new=True)[:6]
    slider_collections = Collection.objects.filter(in_slide=True)[:2]
    three_collections = Collection.objects.filter(in_slide=False)[:3]   
    products = Product.objects.filter(discount_percent__gte=0).order_by('-discount_percent')[:6]
    all_collections = Collection.objects.all().exclude(pk__in=slider_collections.values('pk')).exclude(pk__in=three_collections.values('pk'))
    blogs = Blog.objects.all()[0:3]
    context = {
        'slider_collections':slider_collections,
        'three_collections':three_collections,
        'new':new,
        'products':products,
        'most_searched':most_searched,
        'best_seller':best_seller,
        'all_collections':all_collections,
        'blogs':blogs
    }
    
    return render(request,'index-2.html',context)

def shopSingle(request,slug):
    product = get_object_or_404(Product,slug=slug)
    context = {
        'product':product
    }
    return render(request,'single-product.html',context)

def shop(request):
    product_list = Product.objects.all()
    if request.GET.get('min_price'):
        product_list = product_list.filter(price__gte=request.GET.get('min_price'))
    if request.GET.get('max_price'):
        product_list = product_list.filter(price__lte=request.GET.get('max_price'))
    if request.GET.get('search'):
        product_list = product_list.filter(name__icontains=request.GET.get('search'))
    if request.GET.get('category'):
        product_list = product_list.filter(category__slug=request.GET.get('category'))
    if request.GET.get('collection'):
        product_list = product_list.filter(collection__slug=request.GET.get('collection'))
    if request.GET.get('brand'):
        product_list = product_list.filter(brand__slug=request.GET.get('brand'))
    if request.GET.get('color'):
        product_list = product_list.filter(color__slug=request.GET.get('color'))
    if request.GET.get('size'):
        product_list = product_list.filter(size__slug=request.GET.get('size'))
    if request.GET.get('order'):
        product_list = product_list.order_by(request.GET.get('order'))

    paginator = Paginator(product_list, 12)
    page = request.GET.get("page", 1)
    products = paginator.get_page(page)
    total_pages = [x+1 for x in range(paginator.num_pages)]    
    categories = Category.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    collections = Collection.objects.all()
    context = {
        'products':products,
        'total_pages':total_pages,
        'categories':categories,
        'colors':colors,
        'sizes':sizes,
        'brands':brands,
        'collections':collections,
    }
    return render(request,'shopgrid.html',context)



# def blogs(request):
    
#     blog_list = Blog.objects.all().only('mainimage','title','content_without_ck','category__name')
#     recent_blogs = Blog.objects.all()[:: -1]
#     categories = Category.objects.all().only('name','id')
#     tags = Tag.objects.all()
    
#     if request.GET.get('blog'):
#         name = request.GET.get('blog')
#         blog_list = blog_list.filter(Q(title__icontains=name) | Q(content_without_ck__icontains=name))
        
#     if request.GET.get('category'):
#         category = request.GET.get('category')
#         blog_list = blog_list.filter(category__id=category)
    
#     if request.GET.get('tag'):
#         tag = request.GET.get('tag')
#         blog_list = blog_list.filter(tag__id__in=tag)
        
#     paginator = Paginator(blog_list, 4)
#     page = request.GET.get("page", 1)
#     blogs = paginator.get_page(page)
#     total_pages = [x+1 for x in range(paginator.num_pages)]
    
#     context = {
#         'blogs':blogs,
#         'total_pages':total_pages,
#         'categories':categories,
#         'recent_blogs':recent_blogs,
#         'tags':tags
#     }
    
#     return render(request,'bloglist.html',context)

