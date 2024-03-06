from django.urls import path
from . import views as storeViews

urlpatterns = [
    path('', storeViews.Home, name='store'),
    path('category/<slug:category_slug>/', storeViews.Home, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', storeViews.Product_Detail, name='Product_Detail'),
    path('search/', storeViews.Search, name='search'),
    path('submit_review/<int:product_id>/', storeViews.submit_review, name='submit_review')
]
