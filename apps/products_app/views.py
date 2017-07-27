from django.shortcuts import render, redirect
from models import *
from ..users_app.models import *
from ..orders_app.models import *
import math
import re
# Create your views here.
def home(request):
    context={
        'categories': Category.objects.all(), 'products':Product.objects.all()
    }
    return render(request, 'products_app/productshome.html', context)

def category(request, id, page):
    allProducts=[]
    productCount=Category.objects.get(id=id).products.all().count()
    allProducts=Category.objects.get(id=id).products.all()[(int(page)-1)*12:((int(page)-1)*12)+12]

    newArr=[]
    for i in range(1,int(math.ceil((productCount/12.0)) + 1)):
        newArr.append(i)
    context={
        'products':allProducts, 'numPages':newArr, 'category': Category.objects.get(id=id), 'currPage':page
    }
    return render(request, 'products_app/listproducts.html', context)

def allprod(request, page):
    productCount=Product.objects.all().count()
    allProducts=Product.objects.all()[(int(page)-1)*12:((int(page)-1)*12)+12]

    newArr=[]
    for i in range(1,int(math.ceil((productCount/12.0)) + 1)):
        newArr.append(i)

    context = {
        'products':allProducts, 'numPages':newArr, 'currPage':page
    }
    return render(request, 'products_app/listproducts.html', context)

def search(request, searchname, page):
    # if searchname == '':
    #     return redirect('/products/all/1')

    productCount=Product.objects.filter(name__regex=r""+searchname+"").count()
    allProducts=Product.objects.filter(name__regex=r""+searchname+"")[(int(page)-1)*12:((int(page)-1)*12)+12]

    newArr=[]
    for i in range(1,int(math.ceil((productCount/12.0)) + 1)):
        newArr.append(i)

    context={
        'products':allProducts, 'numPages':newArr, 'searchitem':searchname, 
    }
    return render(request, 'products_app/searchproducts.html', context)

def product(request, id):
    context={
        'product':Product.objects.get(id=id), 'product2': Product.objects.get(id=id).price*2, 'product3': Product.objects.get(id=id).price*3
    }
    return render(request, 'products_app/productpage.html', context)

def addtocart(request):
    # changed id to request.POST['prodid'] by Art
    if request.method == 'POST':
        prod = Product.objects.get(id=request.POST['prodid'])
        prod.quantity=request.POST['quantity']
        prod.save()
        User.objects.get(id=request.session['user_id']).shoppingCart.products.add(prod)
    return redirect('/carts')

def edit(request, id):
    context={
        'categories': Category.objects.all(), 'product':Product.objects.get(id=id)
    }
    return render(request, 'products_app/editproduct.html', context)

def processEdit(request, id):
    prod=Product.objects.get(id=id)
    prod.name=request.POST['name']
    prod.description=request.POST['description']
    if request.POST['newcategory'] == '':
        prod.category=Category.objects.get(name=request.POST['category'])
    else:
        tempcategory=Category.objects.create(name=request.POST['newcategory'])
        prod.category=tempcategory
    prod.save()
    return redirect('/dashboard/products')

def delete(request, id):
    Product.objects.get(id=id).delete()
    return redirect('/dashboard/products')

def new(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'products_app/newproduct.html', context)

def processNew(request):
    # print request.POST['newcategory']
    if request.POST['newcategory'] == '':
        newcategory=Category.objects.get(name=request.POST['category'])
    else:
        newcategory=Category.objects.create(name=request.POST['newcategory'])

    Product.objects.create(name=request.POST['name'], description=request.POST['desc'], price=request.POST['price'], inventory=request.POST['inventory'], quantity='0', sold='0', image=request.POST['image'], category=newcategory)
    return redirect('/dashboard/products/1')

