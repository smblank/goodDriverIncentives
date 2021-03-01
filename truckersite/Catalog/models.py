from django.db import models
from django.conf import settings

# Create your models here.

class SearchWord(models.Model):
    word = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.word 

class Product(models.Model):
    Name = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Img = models.TextField(null=True)
    keyword = models.ForeignKey(SearchWord, on_delete=models.CASCADE, default='')
    slug = models.SlugField(max_length=1000, unique=False)
    
    def __str__(self):
        return self.Name 
    
class OrderedProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.product 

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    Products = models.ManyToManyField(OrderedProduct)
    Start = models.DateTimeField(auto_now_add=True)
    End = models.DateTimeField()
    Ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username 