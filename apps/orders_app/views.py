from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from ..products_app.models import *
from ..users_app.models import *
from .models import *
import math

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
        errors = ShippingInfo.objects.payment_validator(request.POST)

        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/carts')
        else:
            user = User.objects.get(id=request.session['user_id'])
            shoppingCart = user.shoppingCart
            
            # check if shopping cart is empty
            products = shoppingCart.products.all()
            if len(products) == 0:
                messages.error(request,'Shopping Cart is empty.')
                return redirect('/carts')
            else:
                shoppingCart.user = None
                shoppingCart.save()
                new_shopping_cart = ShoppingCart.objects.create(user=user)

                # create an order
                order = Order(shoppingCart=shoppingCart,status="orderin",total=request.session['cart_total'],user=user)
                order.save()

                shipping = ShippingInfo(first_name = request.POST['shipping_first_name'],last_name = request.POST['shipping_last_name'],address = request.POST['shipping_address'],address2 = request.POST['shipping_address2'],city = request.POST['shipping_city'],state = request.POST['shipping_state'],zipcode = request.POST['shipping_zipcode'],user = user, order = order)
                shipping.save()
                billing = BillingInfo(first_name = request.POST['billing_first_name'],last_name = request.POST['billing_last_name'],address = request.POST['billing_address'],address2 = request.POST['billing_address2'],city = request.POST['billing_city'],state = request.POST['billing_state'],zipcode = request.POST['billing_zipcode'],card = request.POST['card'],security = request.POST['security'],expiration = request.POST['expiration'],user = user, order = order)
                billing.save()

                # process the payment
                print 'Processing the payment'
                print 'Success!'

                # add to quantity of product sold
                for product in products:
                    product.sold += product.quantity
                    product.inventory -= product.quantity
                    product.save()

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


def page_process(request, page_num):

    total_pages = Order.objects.count()
    section_pages=Order.objects.all()[(int(page_num)-1)*10:((int(page_num)-1)*10)+10]

    newArr=[]
    for i in range(1,int(math.ceil((total_pages/10.0)) + 1)):
        newArr.append(i)

    context = {
        'total_pages' : newArr,
        'orders' : section_pages,
        
    }
    return render(request, 'orders_app/searchorders.html', context)

def status_process(request, status, page):
    request.session['statuspage'] = status
    total_pages = Order.objects.filter(status=status).count()
    section_pages = Order.objects.filter(status=status)[(int(page)-1)*10:((int(page)-1)*10)+10]

    newArr=[]
    for i in range(1,int(math.ceil((total_pages/10.0)) + 1)):
        newArr.append(i)

    context = {
        'total_pages' : newArr,
        'orders' : section_pages,
        
    }
    return render(request, 'orders_app/searchorders.html', context)


def search_process(request, searchname, page_num):
    request.session['statuspage'] = searchname
    allOrders = []
    tempUsers = User.objects.filter(first_name__regex=r''+searchname+'')
    for user in tempUsers:
        for order in user.orders.all():
            allOrders.append(order)
    orderCount=len(allOrders)
    orderSection=allOrders[(int(page_num)-1)*10:((int(page_num)-1)*10)+10]

    newArr=[]
    for i in range(1,int(math.ceil((orderCount/10.0)) + 1)):
        newArr.append(i)

    context = {
        'total_pages' : newArr,
        'orders' : orderSection,
    }

    return render(request, 'orders_app/searchorders.html', context)

def changestatus(request, id, status):
    print request.session['statuspage']
    if request.session['statuspage'] != 'showall' and request.session['statuspage'] != 'orderin' and request.session['statuspage'] != 'shipped' and request.session['completed']:
        return redirect('/carts/orders/search/'+request.session['search']+'/1')
    if request.session['statuspage'] == 'showall':
        return redirect('/carts/orders/search/1')
    temporder=Order.objects.get(id=id)
    prev=request.session['statuspage']
    temporder.status=status
    temporder.save()
    return redirect('/carts/orders/status/'+prev+'/1')