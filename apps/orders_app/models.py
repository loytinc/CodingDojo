from __future__ import unicode_literals

from django.db import models
from ..products_app.models import *
from ..users_app.models import *

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
noNumberPls = re.compile(r'^[a-zA-Z]+$')

# Create your models here.
class ShoppingCartManager(models.Manager):
    def payment_validator(self, postData):
        errors = []

        if 'shipping_first_name' in postData:
            if len(postData['shipping_first_name']) == 0:
                errors.append('Please enter your first name.')
            elif len(postData['shipping_first_name']) < 2:
                errors.append('First name should be no fewer than 2 letters')
            elif not noNumberPls.match(postData['shipping_first_name']):
                errors.append('First name should have no numbers or special characters in it.')

        if 'shipping_last_name' in postData:
            if len(postData['shipping_last_name']) == 0:
                errors.append('Please enter your last name.')
            elif len(postData['shipping_last_name']) < 2:
                errors.append('Last name should be no fewer than 2 letters')
            elif not noNumberPls.match(postData['shipping_last_name']):
                errors.append('Last name should have no numbers or special characters in it.')

        if 'shipping_address' in postData:
            if len(postData['shipping_address']) == 0:
                errors.append('Please enter your last name.')
            elif len(postData['shipping_address']) < 2:
                errors.append('Last name should be no fewer than 2 letters')
            elif not noNumberPls.match(postData['shipping_address']):
                errors.append('Last name should have no numbers or special characters in it.')

        


class ShoppingCart(models.Model):
    products = models.ManyToManyField(Product, related_name="shoppingCarts")
    user = models.OneToOneField(User, related_name="shoppingCart",null=True)
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
    user = models.ForeignKey(User, related_name="orders", null=True)
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
    order = models.OneToOneField(Order, related_name="billingInfo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
