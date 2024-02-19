from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length = 255)
    slug = models.SlugField(max_length=255)
    description=models.TextField(max_length= 255, blank = True)
    cart_image=models.ImageField(upload_to='photos/cartegories', blank =True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def geturl(self):
        return reverse('products_by_category', args =  [self.slug])

    def __str__(self):
        return self.category_name