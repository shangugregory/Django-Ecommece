from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length = 233, unique=True)
    slug=models.SlugField(max_length = 233, unique=True)
    description = models.TextField(max_length = 500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/product')
    stock = models.IntegerField()
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date= models.DateTimeField(auto_now_add = True)
    modified_date= models.DateTimeField(auto_now = True)
    is_available = models.BooleanField()

    def get_url(self):
        return reverse('Product_Detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
class variationmanager(models.Manager):
    def colors(self):
        return super(variationmanager, self).filter(variation_cartegory = 'color', is_active = True)

    def sizes(self):
        return super(variationmanager, self).filter(variation_cartegory='size', is_active = True)   

variation_cartegory_choice = (
    ('color','color'),
    ('size', 'size')
)
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_cartegory=models.CharField(max_length = 100, choices = variation_cartegory_choice)
    variation_value= models.CharField(max_length=200)
    is_active=models.BooleanField(default = True)
    created_at=models.DateField(auto_now = True)

    objects = variationmanager()

    def __str__(self):
        return self.variation_value