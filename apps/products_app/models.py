from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Product(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2)
    quantity=models.IntegerField()
    image=models.CharField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    category=models.ForeignKey(Category, related_name='products')

