from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def shoppingCart(request):
    return render(request, 'orders_app/shoppingcart.html')
