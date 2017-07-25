from django.shortcuts import render
from models import *
# Create your views here.
def home(request):
    context={
        'categories': Category.objects.all(),
    }
    return render(request, 'products_app/productshome.html', context)

def category(request, id, page):
    allProducts=[]
    products=Category.objects.get(id=id).products
    for i in range(10*(page-1), 10*(page-1) + 11): #product in category.products:
        if i < len(products):
            allProducts.append([products[i].name, products[i].price, products[i].image])

    context={
        'products':allProducts, 'numPages':len(products)/10, 'category': Category.objects.get(id=id)
    }
    return render(request, 'products_app/listproducts.html', context)

def allprod(request, page):
    allProducts=[]
    products=Product.objects.all()
    for i in range(10*(page-1), 10*(page-1) + 11): #product in category.products:
        if i < len(products):
            allProducts.append([products[i].name, products[i].price, products[i].image])

    context={
        'products':allProducts, 'numPages':len(products)/10, 'category': Category.objects.get(id=id)
    }
    return render(request, 'products_app/listproducts.html', context)

def search(request, searchname, page):
    allProducts=[]
    products=Product.objects.filter(name__startswith=searchname)
    for i in range(10*(page-1), 10*(page-1) + 11): #product in category.products:
        if i < len(products):
            allProducts.append([products[i].name, products[i].price, products[i].image])

    context={
        'products':allProducts, 'numPages':len(products)/10, 'searchitem': searchname, 
    }
    return render(request, 'products_app/listproducts.html', context)

def product(request, id):
    context={
        'product':Product.objects.get(id=id)
    }
    return render(request, 'products_app/productpage.html', context)