
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
    path('orders/', include('orders.urls'))
    
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)