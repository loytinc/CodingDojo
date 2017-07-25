from django.shortcuts import render, redirect, HttpResponse
from ..products_app.models import *
from ..users_app.models import *
from .models import *


# Create your views here.
def shoppingCart(request,user_id):

    shoppingCart = ShoppingCart.objects.get(id=request.session['user_id'])

    total = 0
    for product in shoppingCart.products:
        total += product.get_price_total()

    request.session['cart_total'] = total

    context = {
        'shoppingCart' : shoppingCart,
        'total'        : request.session['cart_total']
    }
    return render(request, 'orders_app/shoppingcart.html')


def checkout(request,user_id):
    if request.method == 'POST':
        # validate the form

        shoppingCart = ShoppingCart.objects.get(id=request.session['user_id'])
        user = User.objects.get(id=request.session['user_id'])
        # create an order
        order = Order(shoppingCart=shoppingCart)
        order.save()

        shipping = ShippingInfo(first_name = request.POST['shipping_first_name'],last_name = request.POST['shipping_last_name'],address = request.POST['shipping_address'],address2 = request.POST['shipping_address2'],city = request.POST['shipping_city'],state = request.POST['shipping_state'],zipcode = request.POST['shipping_zipcode'],user = user,order = order)
        shipping.save()
        billing = BillingInfo(first_name = request.POST['billing_first_name'],last_name = request.POST['billing_last_name'],address = request.POST['billing_address'],address2 = request.POST['billing_address2'],city = request.POST['billing_city'],state = request.POST['billing_state'],zipcode = request.POST['billing_zipcode'],card = request.POST['card'],security = request.POST['security'],expiration = request.POST['expiration'],user = user,order = order)
        billing.save()

        # process the payment
        print 'Processing the payment'
    return redirect('/carts/success')


def checkout_success(request):
    return render(request, 'orders_app/payment_confirmation.html')