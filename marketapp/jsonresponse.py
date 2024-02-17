from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from marketapp.models import Order,OrderItem, Product
import json
from marketapp.forms import Messageform
from django.http import HttpResponse

def update_basket(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, status=False)
        orderitems = order.orderitems.all()
        count = len(orderitems)
    else:
        cart = request.session.get('cart', [])
        count = len(cart)
    return JsonResponse({'orderitems':orderitems,'count':count})


def manage_basket(request, action, product_id):

    product = get_object_or_404(Product, pk=product_id)
  
    data = json.loads(request.body)
    if not request.user.is_authenticated:
        cart = request.session.get('cart', [])
        existing_item = next((item for item in cart if item['product'] == product.id and item['color_id'] == data.get('color') and item['size_id'] == data.get('size')), None)
        
        if existing_item:
            existing_item['quantity'] = int(existing_item['quantity']) + int(data.get('quantity'))
        else:
            product_data = {'product': product.id,'product_quantity':product.quantity,'product_image':product.image.url,'product_name':product.name, 'quantity': data.get('quantity'), 'color_id': data.get('color'), 'size_id': data.get('size')}
            cart.append(product_data)
        request.session['cart'] = cart
        for key, value in request.session.items():
            print(f"{key}: {value}")

        return JsonResponse({'message':'sessionda saxlanildi+'}, status=401)
    else:
    
        user = request.user
  

    order, created = Order.objects.get_or_create(user=user, status=False)
  
    basket = OrderItem.objects.filter(order=order,product=product,color_id=data.get('color'),size_id=data.get('size'))
    
    if action == 'add':

        if not basket.exists():
            data = json.loads(request.body)
            basketitem = OrderItem.objects.create(product=product,order=order,quantity=data.get('quantity'),color_id=data.get('color'),size_id=data.get('size'))
            
            message = 'Product added to basket successfully'
        else:
            basketitem = OrderItem.objects.get(product=product,order=order,color_id=data.get('color'),size_id=data.get('size'))
            basketitem.quantity += int(data.get('quantity'))
            print(data.get('quantity'))
            basketitem.save()
            message = 'Product quantity increased in basket successfully'

    elif action == 'remove':
        if basket.exists():
            basketitem = OrderItem.objects.get(product=product,order=order)
            basketitem.delete()
            message = 'Product removed from basket successfully'
        else:
            message = 'Product doesnt exists'

    # elif action == 'quantity':
    #     basket = Basket.objects.filter(product=product,user=user)
    #     if basket.exists():
    #         basket.quantity = request.POST.get('quantity')
    #         basket.save()
    #         message = 'Product quantity has changed'
    # print(message)
    return JsonResponse({'message': message})

def manage_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if user in product.wishlist.all():
        product.wishlist.remove(user)
        message = "Product removed from wishlist."
        status = 201
        print(201)
    else:
        product.wishlist.add(user)
        message = "Product added to wishlist."
        status = 200
        print(200)

    return JsonResponse({'message': message},status = status)

def fetchwish(request):

    if not request.user.is_authenticated:
        return JsonResponse("You are not authenticated. Please log in.", status=401)
    else:
        count = request.user.wishproducts.all().count()
        print(count,'------------')
    return JsonResponse({'count':str(count)})

def message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data,'--------')
        newmessage = Messageform(data=data)
        if newmessage.is_valid():
            newmessage.save()
        else:
            print(newmessage.errors)
            return HttpResponse(status=405) 
        data = {'message': 'Data saved successfully'}
        return JsonResponse(data)
    else:
        return HttpResponse(status=405) 
    
    