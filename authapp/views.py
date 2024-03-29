from django.shortcuts import render, redirect
from authapp.forms import SignUpForm
from authapp.forms import LoginForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect,HttpResponse, HttpResponseRedirect, get_object_or_404
from marketapp.models import Order,OrderItem,Product,Category
from django.db import transaction
from django.urls import reverse
from django.db import close_old_connections
from marketapp.views import get_instagram_photos,get_order_items
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from django.core.mail import EmailMessage
import json
from celery import shared_task

def pdf_generate(order_id):
    order = Order.objects.get(id=order_id)
    order_items = order.orderitems.all()
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    y_coordinate = 750  # Starting Y coordinate

    for item in order_items:
        product_name = item.product.name
        quantity = item.quantity
        color = item.color
        size = item.size
    
        pdf.drawString(100, y_coordinate, f"Product Name: {product_name}")
        pdf.drawString(100, y_coordinate - 20, f"Quantity: {quantity}")
        pdf.drawString(100, y_coordinate - 40, f"Color: {color}")
        pdf.drawString(100, y_coordinate - 60, f"Size: {size}")
        y_coordinate -= 100

    pdf.drawString(100, y_coordinate, f"username: {order.user.username}")
    pdf.drawString(100, y_coordinate - 20, f"phone: {order.phone_number}")
    pdf.drawString(100, y_coordinate - 40, f"address: {order.address}")

    pdf.showPage()
    
    pdf_filename = f"order_details.pdf"  
    pdf_path = os.path.join(settings.BASE_DIR, 'static', pdf_filename) 

    with open(pdf_path, 'wb') as pdf_file:
        pdf.save()
        pdf_data = buffer.getvalue()
        pdf_file.write(pdf_data)
    buffer.seek(0)
    email = EmailMessage(
        'Sifariş N #{}'.format(order.id),
        'Sifarişin detalları əlavə edilmişdir.',
        settings.EMAIL_HOST_USER,
        ['viktoriassirri@gmail.com'],  # Replace with the recipient email address
    )
    email.attach(pdf_filename, pdf_data, 'application/pdf')
    email.send()
    return buffer


def pdf_generate_notAuth(data):
    print('333333333333333333333333333333333333')
    order_items = data.get('items')
    print('333333333333333333355555555555555555555')
    buffer = BytesIO()
    print('4444444444444444444444444444444444444')
    pdf = canvas.Canvas(buffer, pagesize=letter)
    print('55555555555555555555555555555')
    y_coordinate = 750  # Starting Y coordinate
    print('666666666666666666666666666')
    for item in order_items:
        product_name = item['product']['name']
        quantity = item['quantity']
        color = item['color']['name']
        size = item['size']['name']
    
        pdf.drawString(100, y_coordinate, f"Product Name: {product_name}")
        pdf.drawString(100, y_coordinate - 20, f"Quantity: {quantity}")
        pdf.drawString(100, y_coordinate - 40, f"Color: {color}")
        pdf.drawString(100, y_coordinate - 60, f"Size: {size}")
        y_coordinate -= 100


    pdf.drawString(100, y_coordinate - 20, f"phone: {data.get('phone')}")
    pdf.drawString(100, y_coordinate - 40, f"address: {data.get('address')}")

    pdf.showPage()
    
    pdf_filename = f"order_details.pdf"  
    pdf_path = os.path.join(settings.BASE_DIR, 'static', pdf_filename) 
    print('777777777777777777777777777777777777777777777')
    with open(pdf_path, 'wb') as pdf_file:
        pdf.save()
        pdf_data = buffer.getvalue()
        pdf_file.write(pdf_data)
    print('8888888888888888888888888888888888888')
    buffer.seek(0)
    print('99999999999999999999999999999999999')
    email = EmailMessage(
        'Sifariş',
        'Sifarişin detalları əlavə edilmişdir.',
        settings.EMAIL_HOST_USER,
        ['viktoriassirri@gmail.com'],  
    )
    print('100000000000000000000000000000000000000000000000')
    email.attach(pdf_filename, pdf_data, 'application/pdf')
    print('111111111111111')
    email.send()
    print('12222222222222222222222')
    return buffer


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


def shopping(request,form_name=None):

    if request.method == 'POST':

        if form_name == 'change':
            id = request.POST.get('item_id')
            action = request.POST.get('action')
            item = get_object_or_404(OrderItem,id=id)
            if action == 'add':
                item.quantity += 1
            if action == 'subtract':
                if item.quantity == 1:
                    item.delete()
                    return redirect('shopping')
                else:
                    item.quantity -= 1
            item.save()
            return redirect('shopping')

        elif form_name == 'order':
            try:
    
                order = get_object_or_404(Order,id=int(request.POST.get('order')))
             
                check = request.POST.get('check')
                address = request.POST.get('address')
                phone = request.POST.get('phone')

                if not order.orderitems.exists():
                    messages.error(request, f'Xəta: Səbətdə məhsul yoxdur!')
                    return redirect('shopping')
                if not phone or not len(phone)>6:
                    messages.error(request, f'Xəta: Əlaqə nömrəsinin düzgünlüyünü yoxlayın!')
                    return redirect('shopping')
                if not address:
                    messages.error(request, f'Xəta: Ünvan daxil edin!')
                    return redirect('shopping')
                if not check:
                    messages.error(request, f'Xəta: Məlumatların düzgünlüyünü təsdiqləyin!')
                    return redirect('shopping')

                order.address = address
                order.phone_number = phone
                order.status = True
                order.save()
         
                pdf_generate(order.id)
           
                messages.success(request, 'Sifariş uğurla tamamlandı. Sizinlə tezliklə əlaqə saxlanılacaq !')
                
                return redirect('shopping')
                    
            except Exception as e:
                print(str(e))
                messages.error(request, f'Xəta: Məlumatların düzgünlüyünü yoxlayın !')
                return redirect('shopping')
        
        else:
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
        serialized_orderitems = []
        count = 0
        total = 0
        order = {}

    categories = Category.objects.all()
    instas = get_instagram_photos()
    orderitems = get_order_items(request)

    context={'data':serialized_orderitems,'count':count,'total':total,'categories':categories,'instas':instas,'orderitems':orderitems}

    if request.user.is_authenticated:
        context['order'] = order.id
    

    return render(request, 'shoping-cart.html',context)


def wish(request):
    if not request.user.is_authenticated:
        context = {
            'auth':0
        }
        return render(request,'wishlist.html',context)
    product_list = Product.objects.filter(wishlist=request.user)
    orderitems = get_order_items(request)
    paginator = Paginator(product_list, 12)
    page = request.GET.get("page", 1)
    products = paginator.get_page(page)
    total_pages = [x+1 for x in range(paginator.num_pages)]    
    categories = Category.objects.all()


    instas = get_instagram_photos()
    context = {
        'auth':1,
        'categories':categories,
        'instas':instas,
        'products':products,
        'total_pages':total_pages,
        'categories':categories,
        'orderitems':orderitems
    }
    return render(request,'wishlist.html',context)

def order(request):
    data = json.loads(request.body)
    pdf_generate_notAuth(data)
    return JsonResponse({'message':'ok'})