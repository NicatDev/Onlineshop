from django.shortcuts import render, redirect
from authapp.forms import SignUpForm
from authapp.forms import LoginForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect,HttpResponse, HttpResponseRedirect, get_object_or_404
from marketapp.models import Order,OrderItem,Product,Category,Color,Size
from authapp.models import Code
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
from django.contrib.auth import get_user_model
from .utils import createCode
from django.utils.translation import gettext as _
User = get_user_model()
from django.utils.translation import activate, get_language
from django.conf import settings

def pdf_generate(order_id):


    order = Order.objects.get(id=order_id)
    order_items = order.orderitems.all()
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    y_coordinate = 750   
    pdf.setFontSize(14)
    index = 1
    for item in order_items:
        product_name = item.product.name.replace("ə", "e").replace("ğ", "g").replace('ı','i').replace('ö','o').replace('ü','u').replace('ç','c')
        quantity = item.quantity
        color = item.color
        if color is not None:
            color = color.name.replace("ə", "e").replace("ğ", "g").replace('ı','i').replace('ö','o').replace('ü','u').replace('ç','c')
        else:
            color = 'Mehsul rengi movcud deyil'
        size = item.size
        if size is None:
            size = 'Mehsul olcusu movcud deyil'
        pdf.drawString(100, y_coordinate, f"{index}) Mehsul adi: {product_name}")
        pdf.drawString(100, y_coordinate - 20, f"Mehsul sayi: {quantity}")
        pdf.drawString(100, y_coordinate - 40, f"Reng: {color}")
        pdf.drawString(100, y_coordinate - 60, f"Olcu: {size}")
        y_coordinate -= 100
        index += 1

    pdf.setFontSize(18)
    pdf.drawString(100, y_coordinate, "Musteri melumatlari")
    pdf.setFontSize(14)
    pdf.drawString(100, y_coordinate - 20, f"Istifadeci adi: {order.user.username}")
    pdf.drawString(100, y_coordinate - 40, f"Elaqe nomresi: {order.phone_number}")
    pdf.drawString(100, y_coordinate - 60, f"Unvan: {order.address.replace('ə', 'e').replace('ğ', 'g').replace('ı','i').replace('ö','o').replace('ü','u').replace('ç','c')}")

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
        ['viktoriassirri@gmail.com'], 
    )
    email.attach(pdf_filename, pdf_data, 'application/pdf')
    email.send()
    return buffer


def pdf_generate_notAuth(data):
   
    order_items = data.get('items')
 
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)

    y_coordinate = 750  

    pdf.setFontSize(15)
    index = 1
    for item in order_items:
        product_name = item['product']['name'].replace("ə", "e").replace("ğ", "g").replace('ı','i').replace('ö','o').replace('ü','u').replace('ç','c')
        quantity = item['quantity']
        pdf.drawString(100, y_coordinate, f"{index}) Mehsul adi: {product_name}")
        pdf.drawString(100, y_coordinate - 20, f"Mehsul sayi: {quantity}")
        if len(item['color'])>0:
        
            color = item['color']['name'].replace("ə", "e").replace("ğ", "g").replace('ı','i').replace('ö','o').replace('ü','u').replace('ç','c')
            pdf.drawString(100, y_coordinate - 40, f"Reng: {color}")
        if len(item['size'])>0:
            size = item['size']['name']
            pdf.drawString(100, y_coordinate - 60, f"Olçu: {size}")
            
        y_coordinate -= 100
        index += 1
    pdf.setFontSize(18)
    pdf.drawString(100, y_coordinate, "Musteri melumatlari:")
    pdf.setFontSize(14)
    pdf.drawString(100, y_coordinate - 20, f"Elaqə nomresi: {data.get('phone')}")
    pdf.drawString(100, y_coordinate - 40, f"Unvan: {data.get('address').replace('ə', 'e').replace('ğ', 'g').replace('ı','i').replace('ö','o').replace('ü','u').replace('ç','c')}")

    pdf.showPage()
    
    pdf_filename = f"order_details.pdf"  
    pdf_path = os.path.join(settings.BASE_DIR, 'static', pdf_filename) 

    with open(pdf_path, 'wb') as pdf_file:
        pdf.save()
        pdf_data = buffer.getvalue()
        pdf_file.write(pdf_data)

    buffer.seek(0)

    email = EmailMessage(
        'Sifariş',
        'Sifarişin detalları əlavə edilmişdir.',
        settings.EMAIL_HOST_USER,
        ['viktoriassirri@gmail.com'],  
    )

    email.attach(pdf_filename, pdf_data, 'application/pdf')

    email.send()

    return buffer

def confirm(request,username,code):
    if request.method == 'POST':
        user = User.objects.get(username = username)
  
        if user.code.code == code:
            user.is_active = True
            user.save()
   
        return redirect('home')
    return render(request, 'confirmation.html')

from django.urls import reverse

def register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['username'] = request.POST.get('email')
        form = SignUpForm(data) 
        if form.is_valid():
            email = form.cleaned_data['email']
            form.cleaned_data['username'] = email
            user = form.save()
      
            user.is_active = False
            user.save()
            code = Code.objects.create(user=user,code=createCode(user.username))
            
            email = EmailMessage(
                '{% trans "Qeydiyyatı tamamlamaq üçün linkə daxil olun" %}',
                f'https://victoriassirri.az/auth/tesdiq/{user.username}/{code.code}',
                settings.EMAIL_HOST_USER,
                [user.email],  
            )
            email.send()

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
                    messages.error(request, _('Xəta: Səbətdə məhsul yoxdur!'))
               
                    return redirect('shopping')
                if not phone or not len(phone)>6:
                    messages.error(request, _('Xəta: Əlaqə nömrəsinin düzgünlüyünü yoxlayın!'))
                    
                    return redirect('shopping')
                if not address:
                    messages.error(request, _('Xəta: Ünvan daxil edin!'))
           
                    return redirect('shopping')
                if not check:
           
                    messages.error(request, _('Xəta: Məlumatların düzgünlüyünü təsdiqləyin!'))
                 
                    return redirect('shopping')
                
                order.address = address
                order.phone_number = phone
                order.status = True
                order.save()
                current_language = get_language()
                activate(settings.LANGUAGE_CODE)
                pdf_generate(order.id)
                activate(current_language)
                messages.success(request,  _('Sifariş uğurla tamamlandı. Sizinlə tezliklə əlaqə saxlanılacaq !'))
                
                return redirect('shopping')
                    
            except Exception as e:
     
                messages.error(request,  _('Xəta: Məlumatların düzgünlüyünü yoxlayın !'))

                activate(current_language)
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
               
                'id':orderitem.id
            }
     
            if orderitem.color:
                product_data['color'] = orderitem.color.name
            if orderitem.size:
                product_data['size'] = orderitem.size.name
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
    current_language = get_language()
    activate(settings.LANGUAGE_CODE)
    data = json.loads(request.body)
    for i in range(len(data.get('items'))):
        product = Product.objects.get(id=data.get('items')[0]['product']['id'])
        if data.get('items')[0]['color']:
            color = Color.objects.get(id=data.get('items')[0]['color']['id'])
        if data.get('items')[0]['size']: 
            size = Size.objects.get(id=data.get('items')[0]['size']['id'])
        data.get('items')[i]['product']['name'] = product.name
        data.get('items')[i]['color']['name'] = color.name
        data.get('items')[i]['color']['name'] = size.name
    pdf_generate_notAuth(data)
    activate(current_language)
    return JsonResponse({'message':'ok'})