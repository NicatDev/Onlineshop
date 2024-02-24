from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from marketapp.models import Order,OrderItem, Product
import json
from marketapp.forms import Messageform
from django.http import HttpResponse
from django.core.serializers import serialize
from django.forms.models import model_to_dict
# [{'product': {'id': 2, 'image': '/media/09f75f7dc5b6976da26e049dd2defff2_bnAlD6v.jpg', 'name': 'Pijama'}, 'quantity': 2, 'color': '1', 'size': '2'}]
# [{"model": "marketapp.orderitem", "pk": 7, "fields": {"quantity": 2, "product": 1, "order": 1, "color": 2, "size": 1}}, {"model": "marketapp.orderitem", "pk": 8, "fields": {"quantity": 4, "product": 2, "order": 1, "color": 1, "size": 2}}, {"model": "marketapp.orderitem", "pk": 9, "fields": {"quantity": 1, "product": 1, "order": 1, "color": 1, "size": 1}}]


def update_basket(request):
    # request.session['cart'] = []
    
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

        count = sum(int(orderitem['quantity']) for orderitem in serialized_orderitems)
    else:
        cart = request.session.get('cart', [])
        orderitems = cart
        count = len(cart)
        serialized_orderitems = orderitems
        count = sum(int(orderitem['quantity']) for orderitem in serialized_orderitems)
    print(serialized_orderitems)
    return JsonResponse({'orderitems':serialized_orderitems,'count':count}, safe=False)


def manage_basket(request, action, product_id):

    product = get_object_or_404(Product, pk=product_id)
  
    data = json.loads(request.body)
    if not request.user.is_authenticated:
        cart = request.session.get('cart', [])
        
        existing_item = next((item for item in cart if item['product']['id'] == product.id and item['color'] == data.get('color') and item['size'] == data.get('size')), None)    
        if existing_item:
            existing_item['quantity'] = int(existing_item['quantity']) + int(data.get('quantity'))
            existing_item['total'] = int(data.get('quantity'))*float(product.get_discount_price())
            request.session['cart'] = cart 
            request.session.modified = True
            return JsonResponse({'message':'sessionda sayi artirildi'})
        else:
            product_data = {'product':{'id':product.id,'image':product.get_main_image().url,'name':product.name,'price':float(product.get_discount_price())},'total':int(data.get('quantity'))*float(product.get_discount_price()) , 'quantity': data.get('quantity'), 'color': data.get('color'), 'size': data.get('size')}
            cart.append(product_data)
            request.session['cart'] = cart
        for key, value in request.session.items():
            print(f"{key}: {value}")

            return JsonResponse({'message':'sessionda saxlanildi'})
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
        return JsonResponse({'message':"You are not authenticated. Please log in."}, status=401)
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
    
    