from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from marketapp.models import *
from django.urls import translate_url
from django.db.models import Q,F,FloatField,Count
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Count
from django.conf import settings
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext as _

def set_language(request,lang_code,url):
    next_url = url or '/'
    language = lang_code
    response = redirect(next_url)
    if language:
        response.set_cookie('django_language', language)
    return response

def set_language_form(request):

    next_url = request.POST.get('next') or '/'
    language = request.POST.get('language')
    response = redirect(next_url)
    if language:
        response.set_cookie('django_language', language)
    return response


def get_order_items(request):
  
    orderitems = []
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, status=False)
        if created:
            orderitems = []
            leng = 0
        else:
            orderitems = OrderItem.objects.filter(order=order)
            leng = sum([int(x.quantity) for x in orderitems])
        return {'orderitems':orderitems,'leng':leng}

def get_instagram_photos():
    images = İnstagramPhoto.objects.all()[:6]
    return images


def home(request):
    
    products = Product.objects.all().order_by('-created_at')[0:3]
    best_seller = Product.objects.filter(best_seller=True)[:3]
    most_searched = Product.objects.filter(most_searched=True)[:3]
    new = Product.objects.filter(new=True)[:6]
    slider_collections = Category.objects.filter(in_slide=True)
    three_collections = Collection.objects.filter(in_slide=True)[:3]   
    products = Product.objects.filter(discount_percent__gte=0).order_by('-discount_percent')[:3]
    all_collections = Category.objects.all().exclude(pk__in=slider_collections.values('pk'))
    blogs = Blog.objects.all()[0:3]
    partners = Partner.objects.all()
    orderitems = get_order_items(request)
    categories = Category.objects.all()
    instas = get_instagram_photos()

    context = {
        'categories':categories,
        'instas':instas,
        'orderitems':orderitems,
        'slider_collections':slider_collections,
        'three_collections':three_collections,
        'new':new,
        'products':products,
        'most_searched':most_searched,
        'best_seller':best_seller,
        'all_collections':all_collections,
        'blogs':blogs,
        'partners':partners,
    }
    
    return render(request,'index-2.html',context)

def hello_world(request):
    response_data = {'msg': _('This Url does not exist. Check spelling.')}
    return HttpResponse(response_data)

def shopSingle(request,slug):
    trans = _('hello')
    orderitems = get_order_items(request)
    product = get_object_or_404(Product,slug=slug)
    categories = Category.objects.all()
    instas = get_instagram_photos()
    products = Product.objects.all().order_by('-discount_percent')[:4]
    context = {
        'categories':categories,
        'instas':instas,
        'product':product,
        'orderitems':orderitems,
        'products':products,
        'trans':trans
    }
    return render(request,'single-product.html',context)

def shop(request):
    collection = {}
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
        collection = Collection.objects.get(slug=request.GET.get('collection'))
    if request.GET.get('brand'):
        product_list = product_list.filter(brand__slug=request.GET.get('brand'))
    if request.GET.get('color'):
        product_list = product_list.filter(color__slug=request.GET.get('color'))
    if request.GET.get('size'):
        product_list = product_list.filter(size__slug=request.GET.get('size'))
    if request.GET.get('order'):
        product_list = product_list.order_by(request.GET.get('order'))
    orderitems = get_order_items(request)
    paginator = Paginator(product_list, 12)
    page = request.GET.get("page", 1)
    products = paginator.get_page(page)
    total_pages = [x+1 for x in range(paginator.num_pages)]    
    categories = Category.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    collections = Collection.objects.all()
    instas = get_instagram_photos()
    best_sellers = Product.objects.order_by('best_seller')[:3]
    context = {
        'categories':categories,
        'instas':instas,
        'products':products,
        'total_pages':total_pages,
        'categories':categories,
        'colors':colors,
        'sizes':sizes,
        'brands':brands,
        'collections':collections,
        'orderitems':orderitems,
        'collection':collection,
        'best_sellers':best_sellers
    }
    return render(request,'shopgrid.html',context)

def contact(request):
    orderitems = get_order_items(request)
    categories = Category.objects.all()
    instas = get_instagram_photos()
    context = {
        'categories':categories,
        'instas':instas,
        'orderitems':orderitems
    }
    return render(request,'contact.html',context)

def about(request):
    instas = get_instagram_photos()
    context = {
        'instas':instas
    }
    return render(request,'about.html',context)

def blogs(request):
    
    blog_list = Blog.objects.all()
    recent_blogs = Blog.objects.all()[:: -1]
    tags = BlogTag.objects.all().only('name','id')
    products = Product.objects.all()[:3]
    
    if request.GET.get('blog'):
        name = request.GET.get('blog')
        blog_list = blog_list.filter(Q(title__icontains=name) | Q(content_without_ck__icontains=name))
        
    if request.GET.get('tag'):
        tag = request.GET.get('tag')
        blog_list = blog_list.filter(tag__name=tag)
    
        
    paginator = Paginator(blog_list, 1)
    page = request.GET.get("page", 1)
    blogs = paginator.get_page(page)
    total_pages = [x+1 for x in range(paginator.num_pages)]
    blogs_not_in_current_page = Blog.objects.exclude(id__in=[x.id for x in blogs])[:3]
    orderitems = get_order_items(request)
    categories = Category.objects.all()
    instas = get_instagram_photos()
    context = {
        'categories':categories,
        'instas':instas,
        'orderitems':orderitems,
        'blogs':blogs,
        'products':products,
        'total_pages':total_pages,
        'tags':tags,
        'recent_blogs2':recent_blogs,
        'recent_blogs':blogs_not_in_current_page
    }
    
    return render(request,'blog.html',context)


def blogSingle(request,slug):
    
    blog = get_object_or_404(Blog,slug=slug)
    tags = BlogTag.objects.all()
    
    orderitems = get_order_items(request)
    categories = Category.objects.all()
    instas = get_instagram_photos()
    context = {
        'categories':categories,
        'instas':instas,
        'orderitems':orderitems,
        'tags':tags,
        'blog':blog,
       
    }
    if len(Blog.objects.all())>2:
        pre = Blog.objects.exclude(id=blog.id).first()
        
        next = Blog.objects.exclude(id=blog.id).exclude(id=pre.id).first()
        context['pre'] = pre
        context['next'] = next
    return render(request,'blog-details.html',context)


