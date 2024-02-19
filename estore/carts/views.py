from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from .models import Cart as MyCart, CartItem 
from store.models import Variation
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)#get product
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value= request.POST[key]
            try:
                variation = Variation.objects.get(product= product, variation_cartegory__iexact = key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    
    try:
        cart = MyCart.objects.get(cart_id =_cart_id(request))#get the cart using the cart id present

    except ObjectDoesNotExist:
        cart = MyCart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except ObjectDoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id):
    cart = MyCart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id= product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = MyCart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.delete()
    return redirect('cart')
def Cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        cart = MyCart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price *cart_item.quantity)
            quantity +=cart_item.quantity
        tax = (2*total/100)
        grant_total = total +tax
    except ObjectDoesNotExist:
        pass

    context ={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'grant_total':grant_total,
        'tax':tax
    }

    return render(request, 'home/cart.html', context)
