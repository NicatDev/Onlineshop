from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from marketapp.models import Basket, Product


def manage_basket(request, action, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    basket = Basket.objects.filter(product=product,user=user)
    if action == 'add':
        if not basket.exists():
            basketitem = Basket.objects.create(product=product,user=user,quantity=1)
            message = 'Product added to basket successfully'
        else:
            message = 'Product has been already exists'

    elif action == 'remove':
        basket = Basket.objects.filter(product=product,user=user)
        if basket.exists():
            basketitem = Basket.objects.get(product=product,user=user)
            basketitem.delete()
            message = 'Product removed from basket successfully'
        else:
            message = 'Product doesnt exists'

    elif action == 'quantity':
        basket = Basket.objects.filter(product=product,user=user)
        if basket.exists():
            basket.quantity = request.POST.get('quantity')
            basket.save()
            message = 'Product quantity has changed'
    print(message)
    return JsonResponse({'message': message})

def manage_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if user in product.wishlist.all():
        product.wishlist.remove(user)
        message = "Product removed from wishlist."
        status = 201
    else:
        product.wishlist.add(user)
        message = "Product added to wishlist."
        status = 200

    return JsonResponse({'message': message},status = status)