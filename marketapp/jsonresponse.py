from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from marketapp.models import Order,OrderItem, Product
import json
from marketapp.forms import Messageform
from django.http import HttpResponse
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
# [{'product': {'id': 2, 'image': '/media/09f75f7dc5b6976da26e049dd2defff2_bnAlD6v.jpg', 'name': 'Pijama'}, 'quantity': 2, 'color': '1', 'size': '2'}]
# [{"model": "marketapp.orderitem", "pk": 7, "fields": {"quantity": 2, "product": 1, "order": 1, "color": 2, "size": 1}}, {"model": "marketapp.orderitem", "pk": 8, "fields": {"quantity": 4, "product": 2, "order": 1, "color": 1, "size": 2}}, {"model": "marketapp.orderitem", "pk": 9, "fields": {"quantity": 1, "product": 1, "order": 1, "color": 1, "size": 1}}]

def add_basket(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        user = request.user
        data = request.data
        
        order, created = Order.objects.get_or_create(user=user, status=False)
        basket = OrderItem.objects.filter(order=order,product_id=data.get('product'),color_id=data.get('color'),size_id=data.get('size'))
        if not basket.exists():
            basketitem = OrderItem.objects.create(order=order,product_id=data.get('product'),color_id=data.get('color'),size_id=data.get('size'))
            message = 'Uğurla əlavə olundu !'
        else:
            basketitem = OrderItem.objects.get(order=order,product_id=data.get('product'),color_id=data.get('color'),size_id=data.get('size'))
            basketitem.quantity += int(data.get('quantity'))
            basketitem.save()
            message = 'Uğurla sayı artırıldı'
        return JsonResponse({'status': 'success', 'message':message})
        
def add_wish(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
        product_id = request.POST.get('id', '')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product does not exist'})

        user = request.user
 
        if product in user.wishproducts.all():
            user.wishproducts.remove(product)
            action = 'removed'
            
        else:
            user.wishproducts.add(product)
            action = 'added'
        length = len(user.wishproducts.all())
        return JsonResponse({'status': 'success', 'action': action,'len':length})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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
    
