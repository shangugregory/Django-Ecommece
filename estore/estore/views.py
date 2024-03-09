from django.shortcuts import render
from store.models import Product, ReviewRatings
from category.models import Category

def Home(request):

    product=Product.objects.all().filter(is_available=True).order_by('created_date')

    for products in product:
        reviews = ReviewRatings.objects.filter(product_id=products.id, status=True)

    context={
        'product':product,
        'products':products
}
    return render(request, 'home/index.html', context)
