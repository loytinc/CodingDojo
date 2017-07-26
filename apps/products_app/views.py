from django.shortcuts import render, redirect
from models import *
# Create your views here.
def home(request):
    context={
        'categories': Category.objects.all(), 'products':Product.objects.all()
    }
    return render(request, 'products_app/productshome.html', context)

def category(request, id, page):
    allProducts=[]
    productCount=Category.objects.get(id=id).products.count()
    allProducts=Category.objects.get(id=id).products[(page-1)*10:((page-1)*10)+10]
    # for i in range(10*(page-1), 10*(page-1) + 11): #product in category.products:
    #     if i < len(products):
    #         allProducts.append([products[i].name, products[i].price, products[i].image])

    context={
        'products':allProducts, 'numPages':productCount/10, 'category': Category.objects.get(id=id)
    }
    return render(request, 'products_app/listproducts.html', context)

def allprod(request, page):
    # allProducts=[]
    productCount=Product.objects.all().count()
    allProducts=Product.objects.all()[(page-1)*10:((page-1)*10)+10]
    # for i in range(10*(page-1), 10*(page-1) + 11): #product in category.products:
    #     if i < len(products):
    #         allProducts.append([products[i].name, products[i].price, products[i].image])

    context={
        'products':allProducts, 'numPages':productCount/10, 'category': Category.objects.get(id=id)
    }
    return render(request, 'products_app/listproducts.html', context)

def search(request, searchname, page):
    # allProducts=[]
    productCount=Product.objects.filter(name__startswith=searchname).count()
    allProducts=Product.objects.filter(name__startswith=searchname)[(page-1)*10:((page-1)*10)+10]
    # for i in range(10*(page-1), 10*(page-1) + 11): #product in category.products:
    #     if i < len(products):
    #         allProducts.append([products[i].name, products[i].price, products[i].image])

    context={
        'products':allProducts, 'numPages':productCount/10, 'searchitem':searchname, 
    }
    return render(request, 'products_app/listproducts.html', context)

def product(request, id):
    context={
        'product':Product.objects.get(id=id)
    }
    return render(request, 'products_app/productpage.html', context)

def addtocart(request):
    prod = Product.objects.get(id=id)
    prod.quantity=request.POST['quantity']
    prod.save()
    User.objects.get(id=request.session['user_id']).shoppingCart.products.add(prod)
    return redirect('prodcuts/all/1')