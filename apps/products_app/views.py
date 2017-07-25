from django.shortcuts import render
from models import *
# Create your views here.
def home(request):
    context={
        'categories': Category.objects.all(),
    }
    return render(request, 'products_app/productshome.html')

def category(request, id, page):
    allProducts=[]
    products=Category.objects.get(id=id).products
    for i in range(10*(page-1), 10*(page-1) + 11): #product in category.products:
        allProducts.append([products[i].name, products[i].price, products[i].image])

    context={
        'products':allProducts, 'numPages':len(allProducts)/10, 'category': Category.objects.get(id=id)
    }
    return render(request, 'products_app/listproducts.html', context)

def product(request, id):
    return render(request, 'products_app/listproducts.html')

def search(request, id):
    allProducts=[]
    products=Category.objects.filter(name__startswith=request.POST['name'])
    for i in range(10*(page-1), 10*(page-1) + 11): #product in category.products:
        allProducts.append([products[i].name, products[i].price, products[i].image])

    context={
        'products':allProducts, 'numPages':len(allProducts)/10, 'category': Category.objects.get(id=id)
    }
    return render(request, 'products_app/listproducts.html', context)