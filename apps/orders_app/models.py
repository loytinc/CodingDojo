from __future__ import unicode_literals

from django.db import models
from ..products_app.models import *
from ..users_app.models import *

# Create your models here.
class ShoppingCart(models.Model):
    products = models.ManyToManyField(Product, related_name="orders")
    user = models.OneToOneField(User, related_name="shoppingCart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        if self.products:
            total = 0
            for product in self.products:
                total += product.get_price_total()

            return total

class Order(models.Model):
    shoppingCart = models.OneToOneField(ShoppingCart, related_name="order")
    status = models.CharField(max_length=150,null=True,blank=True)
    total  = models.DecimalField(max_digits=10, decimal_places=2,null=True)
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
