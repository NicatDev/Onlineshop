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
    
