from django.shortcuts import render
from store.models import Product
from category.models import Category

def Home(request):
    product=Product.objects.all().filter(is_available=True)
    
    context={'product':product,}
    return render(request, 'home/index.html', context)

def Dashboard(request):
    return render(request, 'home/dashboard.html', {})

def OrderCompleted(request):
    return render(request, 'home/orde_completed.html', {})

def PlaceOrder(request):
    return render(request, 'home/place-order.html', {})

def ProductDetail(request):
    return render(request, 'home/product-detail.html', {})


def Store(request):
    return render(request, 'home/store.html', {})