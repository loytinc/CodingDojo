from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def amount(self):
        print self.products
        return len(self.products.all())
    
class Product(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.IntegerField()
    inventory=models.IntegerField()
    sold=models.IntegerField()
    image=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    category=models.ForeignKey(Category, related_name='products')

    def get_price_total(self):
        return self.price*self.quantity