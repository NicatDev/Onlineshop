from django.shortcuts import render, redirect
from authapp.forms import SignUpForm
from authapp.forms import LoginForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from marketapp.models import Order,OrderItem,Product,Category
from django.db import transaction
from django.urls import reverse
from django.db import close_old_connections
from marketapp.views import get_instagram_photos,get_order_items
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['username'] = request.POST.get('email')
        form = SignUpForm(data) 
        if form.is_valid():
            email = form.cleaned_data['email']
            form.cleaned_data['username'] = email
            user = form.save()
            
            
            
            
            return JsonResponse({'success': True}) 
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    return render(request,'login.html',{})


def logout_view(request):
    logout(request)
    return redirect('home')


def shopping(request):
    if request.method == 'POST':
        order, created = Order.objects.get_or_create(user=request.user, status=False)
        basket = OrderItem.objects.filter(order=order)
        for item in basket:
            item.delete()
        return redirect('shopping')
    
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, status=False)
        orderitems = order.orderitems.all()
        
        serialized_orderitems = []

        for orderitem in orderitems:
            product_data = {
                'product':{
                'id':orderitem.product.id,
                'image':orderitem.product.get_main_image().url,
                'name': orderitem.product.name,
                'price':orderitem.product.get_discount_price()},
                
                'total':orderitem.quantity*orderitem.product.get_discount_price(),
                'quantity': orderitem.quantity,
                'color':orderitem.color.name,
                'size':orderitem.size.name,
                'id':orderitem.id
            }
            serialized_orderitems.append(product_data)

        count = sum(orderitem['quantity'] for orderitem in serialized_orderitems)
        total = sum(orderitem['total'] for orderitem in serialized_orderitems)
        
    else:
        cart = request.session.get('cart', [])
        orderitems = cart
        count = len(cart)
        serialized_orderitems = orderitems
        count = sum(int(orderitem['quantity']) for orderitem in serialized_orderitems)
        total = 0
    categories = Category.objects.all()
    instas = get_instagram_photos()
    orderitems = get_order_items(request)

    return render(request, 'shoping-cart.html',context={'data':serialized_orderitems,'count':count,'total':total,'categories':categories,'instas':instas,'orderitems':orderitems})


def wish(request):
    product_list = Product.objects.filter(wishlist=request.user)
    orderitems = get_order_items(request)
    paginator = Paginator(product_list, 12)
    page = request.GET.get("page", 1)
    products = paginator.get_page(page)
    total_pages = [x+1 for x in range(paginator.num_pages)]    
    categories = Category.objects.all()


    instas = get_instagram_photos()
    context = {
        'categories':categories,
        'instas':instas,
        'products':products,
        'total_pages':total_pages,
        'categories':categories,
        'orderitems':orderitems
    }
    return render(request,'wishlist.html',context)