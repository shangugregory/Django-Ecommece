from django.contrib import admin
from . models import Product, Variation, ReviewRatings,ProductGalery
import admin_thumbnails
# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalaryInline(admin.TabularInline):
    model = ProductGalery
    extra = 1
class ProductAdmin(admin.ModelAdmin):
    list_display =('product_name', 'price',  'stock', 'category', 'modified_date')
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ProductGalaryInline]

admin.site.register(Product, ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display =(
        'product', 
        'variation_cartegory',  
        'variation_value', 
        'is_active', 
    )
    list_editable = (
        'is_active',
        'variation_cartegory',  
        'variation_value', 
    )
    list_filter = (
        'product', 
        'variation_cartegory',  
        'variation_value', 
       
    )




admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRatings)
admin.site.register(ProductGalery)
