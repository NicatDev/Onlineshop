from django.shortcuts import render, redirect
from authapp.forms import SignUpForm
from authapp.forms import LoginForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from marketapp.models import Order,OrderItem
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                orderhead, created = Order.objects.get_or_create(user=user, status=False)
               
                cart = request.session.get('cart', [])
                print(cart,'+++++++++++++++=')
                print(cart)
                if cart:
                    for order in cart:
                        print(order)
                        print(order['product'])
                        OrderItem.objects.create(product_id=order['product']['id'],size_id=order['size'],color_id=order['color'],quantity=order['quantity'],order=orderhead)
                        
                
                messages.success(request, 'Logged in successfully')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False,'errors':{'Xəta':["Yanlış ad və ya şifrə"]}})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def shopping(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, status=False)
        orderitems = order.orderitems.all()
        
        serialized_orderitems = []

        for orderitem in orderitems:
            product_data = {
                'product':{
                'id':orderitem.product.id,
                'image':orderitem.product.get_main_image().url,
                'name': orderitem.product.name,},
                'quantity': orderitem.quantity,
                'color':orderitem.color.id,
                'size':orderitem.size.id
            }
            serialized_orderitems.append(product_data)

        count = sum(orderitem['quantity'] for orderitem in serialized_orderitems)
        
    else:
        cart = request.session.get('cart', [])
        orderitems = cart
        count = len(cart)
        serialized_orderitems = orderitems
        count = sum(int(orderitem['quantity']) for orderitem in serialized_orderitems)
    print(serialized_orderitems,'999')
    return render(request, 'shoping-cart.html',context={'data':serialized_orderitems,'count':count})
