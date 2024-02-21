
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views as home_views
from store.views import Home as storeViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.Home, name= 'home'),
    path('account/', include('accounts.urls')),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('dashboard', home_views.Dashboard, name='dashboard'),
    path('order_completed', home_views.OrderCompleted, name='orde_completed'),
    path('place_order', home_views.PlaceOrder, name='place_order'),
    path('product', home_views.ProductDetail, name='product'),
    
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)