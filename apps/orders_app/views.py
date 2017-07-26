from django.shortcuts import render, redirect, HttpResponse
from ..products_app.models import *
from ..users_app.models import *
from .models import *


# Create your views here.

# shopping cart
def shoppingCart(request):

    shoppingCart = User.objects.get(id=request.session['user_id']).shoppingCart

    total = 0
    for product in shoppingCart.products.all():
        total += product.get_price_total()

    request.session['cart_total'] = float(total)

    context = {
        'shoppingCart' : shoppingCart,
        'total'        : request.session['cart_total']
    }
    return render(request, 'orders_app/shoppingcart.html',context)


def checkout(request):
    if request.method == 'POST':
        # validate the form

        shoppingCart = ShoppingCart.objects.get(id=request.session['user_id'])
        user = User.objects.get(id=request.session['user_id'])
        # create an order
        order = Order(shoppingCart=shoppingCart,status="orderin",total=request.session['cart_total'])
        order.save()

        shipping = ShippingInfo(first_name = request.POST['shipping_first_name'],last_name = request.POST['shipping_last_name'],address = request.POST['shipping_address'],address2 = request.POST['shipping_address2'],city = request.POST['shipping_city'],state = request.POST['shipping_state'],zipcode = request.POST['shipping_zipcode'],user = user, order = order)
        shipping.save()
        billing = BillingInfo(first_name = request.POST['billing_first_name'],last_name = request.POST['billing_last_name'],address = request.POST['billing_address'],address2 = request.POST['billing_address2'],city = request.POST['billing_city'],state = request.POST['billing_state'],zipcode = request.POST['billing_zipcode'],card = request.POST['card'],security = request.POST['security'],expiration = request.POST['expiration'],user = user, order = order)
        billing.save()

        # process the payment
        print 'Processing the payment'
    return redirect('/carts/checkout/success')


def checkout_success(request):
    return render(request, 'orders_app/payment_confirmation.html')




# Order tracking
def track_orders(request):
    orders = Order.objects.all()
    
    context = {
        'orders' : orders
    }
    return render(request, 'orders_app/order_tracker.html',context)


def update_status(request):
    if request.method == 'POST':
        order = Order.objects.get(id=request.POST['order_id'])
        order.status = request.POST['status']
        order.save()
    return redirect('/carts/orders')


def view_order(request, order_id):
    order = Order.objects.get(id=order_id)
    products = order.shoppingCart.products.all()
    context = {
        'order' : order,
        'products' : products
    }
    return render(request, 'orders_app/view_order.html', context)