from __future__ import unicode_literals

from django.db import models
from ..products_app.models import *
from ..users_app.models import *

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
noNumberPls = re.compile(r'^[a-zA-Z ]+$')
numbersOnly = re.compile(r'[\d]+')

# Create your models here.
class ShoppingCartManager(models.Manager):
    def payment_validator(self, postData):
        errors = []

        if 'shipping_first_name' in postData:
            if len(postData['shipping_first_name']) == 0:
                errors.append('Please enter your first name.')
            elif len(postData['shipping_first_name']) < 2:
                errors.append('Shipping first name should be no fewer than 2 letters')
            elif not noNumberPls.match(postData['shipping_first_name']):
                errors.append('Shipping first name should only contain letters.')

        if 'shipping_last_name' in postData:
            if len(postData['shipping_last_name']) == 0:
                errors.append('Please enter your last name.')
            elif len(postData['shipping_last_name']) < 2:
                errors.append('Shipping last name should be no fewer than 2 letters')
            elif not noNumberPls.match(postData['shipping_last_name']):
                errors.append('Shipping last name should only contain letters.')

        if 'shipping_address' in postData:
            if len(postData['shipping_address']) == 0:
                errors.append('Please enter your shipping address.')

        if 'shipping_city' in postData:
            if len(postData['shipping_city']) == 0:
                errors.append('Please enter your shipping city.')
            elif not noNumberPls.match(postData['shipping_city']):
                errors.append('Shipping city should only contain letters.')

        if 'shipping_state' in postData:
            if len(postData['shipping_state']) == 0:
                errors.append('Please enter your shipping state.')
            elif not noNumberPls.match(postData['shipping_state']):
                errors.append('Shipping state should only contain letters.')

        if 'shipping_zipcode' in postData:
            if len(postData['shipping_zipcode']) == 0:
                errors.append('Please enter your shipping zip code.')
            elif len(postData['shipping_zipcode']) != 5:
                errors.append('Shipping zip code must be a 5 digit number.')
            elif not numbersOnly.match(postData['shipping_zipcode']):
                errors.append('Shipping zip code should only be in numbers.')

        # billing validation
        
        if 'billing_first_name' in postData:
            if len(postData['billing_first_name']) == 0:
                errors.append('Please enter your first name.')
            elif len(postData['billing_first_name']) < 2:
                errors.append('Billing first name should be no fewer than 2 letters')
            elif not noNumberPls.match(postData['billing_first_name']):
                errors.append('First name should only contain letters.')

        if 'billing_last_name' in postData:
            if len(postData['billing_last_name']) == 0:
                errors.append('Please enter your last name.')
            elif len(postData['billing_last_name']) < 2:
                errors.append('Billing last name should be no fewer than 2 letters')
            elif not noNumberPls.match(postData['billing_last_name']):
                errors.append('Billing last name should only contain letters.')

        if 'billing_address' in postData:
            if len(postData['billing_address']) == 0:
                errors.append('Please enter your billing address.')

        if 'billing_city' in postData:
            if len(postData['billing_city']) == 0:
                errors.append('Please enter your billing city.')
        elif not noNumberPls.match(postData['billing_city']):
                errors.append('Billing city should only contain letters.')

        if 'billing_state' in postData:
            if len(postData['billing_state']) == 0:
                errors.append('Please enter your billing state.')
            elif not noNumberPls.match(postData['billing_state']):
                errors.append('Billing state should only contain letters.')

        if 'billing_zipcode' in postData:
            if len(postData['billing_zipcode']) == 0:
                errors.append('Please enter your billing zip code.')
            elif len(postData['billing_zipcode']) != 5:
                errors.append('Billing zip code must be a 5 digit number.')
            elif not numbersOnly.match(postData['billing_zipcode']):
                errors.append('Billing zip code should only be in numbers.')

        if 'card' in postData:
            if len(postData['card']) == 0:
                errors.append('Please enter your 16 digit credit card number.')
            elif len(postData['card']) != 16:
                errors.append('Please enter 16 digits for your credit card number.')
            elif not numbersOnly.match(postData['card']):
                errors.append('Card entry should only be in numbers.')

        if 'security' in postData:
            if len(postData['security']) == 0:
                errors.append('Please enter your three digit security number on the back of your card.')
            elif len(postData['security']) != 3:
                errors.append('Please enter 3 digits for your security number.')
            elif not numbersOnly.match(postData['security']):
                errors.append('Security code should only be in numbers.')

        if 'expiration' in postData:
            if len(postData['expiration']) == 0:
                errors.append('Please enter your credit card expiration date.')
            else:
                expiration = postData['expiration']
                date_format = "%Y-%m-%d"
                expire = datetime.strptime(expiration, date_format).date()
                now = datetime.now().date()

                if expire < now:
                    errors.append('Expiration Date cannot be in the past.')
                elif expire == now:
                    errors.append('Expiration Date cannot be today')
        return errors


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
    objects = ShoppingCartManager()

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
    objects = ShoppingCartManager()

class Quantity(models.Model):
    amount = models.IntegerField()
    shopping_cart = models.ForeignKey(ShoppingCart, related_name="quantities")
    product = models.ForeignKey(Product, related_name="quantities")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def get_price_total(self):
        return self.product.price*self.amount