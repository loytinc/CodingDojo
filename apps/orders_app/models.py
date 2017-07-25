from __future__ import unicode_literals

from django.db import models
from ..products_app.models import *
from ..users_app.models import *

# Create your models here.
class ShoppingCart(models.Model):
    total = models.IntegerField()
    products = models.ManyToManyField(Product, related_name="orders")
    user = models.ForeignKey(User, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    shoppingCart = models.OneToOneField(ShoppingCart, related_name="order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ShippingInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.IntegerField()
    user = models.ForeignKey(User, related_name="shippingInfos")
    order = models.OneToOneField(Order, related_name="shippingInfo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BillingInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.IntegerField()
    card = models.IntegerField()
    security = models.IntegerField()
    expiration = models.DateField()
    user = models.ForeignKey(User, related_name="billingInfos")
    order = models.OneToOneField(User, related_name="billingInfo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
