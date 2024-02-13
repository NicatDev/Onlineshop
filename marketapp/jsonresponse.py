from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from marketapp.models import Order,OrderItem, Product


def manage_basket(request, action, product_id):

    product = get_object_or_404(Product, pk=product_id)
  
    if not request.user.is_authenticated:
        
        return JsonResponse("You are not authenticated. Please log in.", status=401)
    else:
    
        user = request.user
    order, created = Order.objects.get_or_create(user=user, status=False)
    basket = OrderItem.objects.filter(order=order,product=product)
    if action == 'add':
        
        if not basket.exists():
            basketitem = OrderItem.objects.create(product=product,order=order,quantity=1)
            message = 'Product added to basket successfully'
        else:
            basketitem = OrderItem.objects.get(product=product,order=order)
            basketitem.quantity += 1
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