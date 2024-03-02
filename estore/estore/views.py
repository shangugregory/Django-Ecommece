from django.shortcuts import render
from store.models import Product
from category.models import Category

def Home(request):
    product=Product.objects.all().filter(is_available=True)
    
    context={'product':product,}
    return render(request, 'home/index.html', context)
