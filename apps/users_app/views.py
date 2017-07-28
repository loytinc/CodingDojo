from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django import forms
from django.contrib import messages
import datetime
from time import gmtime, strftime
import re
from models import User

from django.shortcuts import render, redirect, HttpResponse
from .models import User
from ..products_app.models import *
from ..orders_app.models import *
from django.contrib import messages
import bcrypt
import math

def index(request):
    return render(request, 'userDashboard/index.html')

def dashboard(request):
    #user must be logged in and must be an admin to see page
    if request.session.get('user_id', False):
        user = User.objects.get(id=request.session['user_id'])
        if user.user_level == 9:
            context = {
               'users': User.objects.all()
            }
            return render(request, 'userDashboard/dashboard.html', context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def prodDashboard(request):
    context={
        'products':Product.objects.all()#, 'numPages':newArr
    }
    return render(request, 'userDashboard/productDash.html', context)

def signin(request):
    if 'user_id' in request.session:
        if request.session['isAdmin'] == True:
            return redirect('/dashboard')
        return redirect('/products')
    return render(request, 'userDashboard/login.html')

def register(request):
    return render(request, 'userDashboard/registration.html')

def create_user(request):
    if request.method == 'POST':

        # validate all form data
        errors = User.objects.user_validator(request.POST)

        # populate messages with errors or specifics if true
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/register')
        else:
        # if errors FREE
            try:
                # does email already exist in database
                check_email = User.objects.get(email = request.POST['email'])
                messages.error(request, 'Please try another email input.')

                return redirect('/index')

            except:
                users = User.objects.count()

                #if the user count is less than 4, the next user created with become an admin
                if users < 4:
                    user_level=9
                else:
                    user_level=1


                # hash password
                hash_it = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                
                # insert user into database
                user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'],birthday=request.POST['birthday'],user_level=user_level,password=hash_it)
                user.save()
                
                # assign a shopping cart for the user by Art
                shoppingCart = ShoppingCart(user=user)
                shoppingCart.save()

                messages.success(request, 'You have successfully registered')
    return redirect('/register')

def user(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')

        return redirect('/index')

    user = User.objects.get(id=user_id)

    context = {
        'user' : user,
    }
    return render(request, 'users_app/user.html', context)

def edit_user(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])

    context = {
        'current_user_id' : request.session['user_id'],
        'user'            : user,
    }

    return render(request, 'userDashboard/edit_user.html', context)


def edit_user_admin(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('/')

    if request.session['isAdmin'] == False:
        return redirect('/dashboard')

    user = User.objects.get(id=user_id)

    context = {
        'current_user_id' : request.session['user_id'],
        'user'            : user,
    }

    return render(request, 'userDashboard/admin_edit_user.html', context)


def profile(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('/')

    owner = User.objects.get(id=user_id)

    context = {
        'current_user_id' : request.session['user_id'],
        'user' : owner,
    }

    return render(request, 'userDashboard/profile.html', context)

def warning(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('/')

    if request.session['isAdmin'] == False:
        return redirect('/dashboard')

    user = User.objects.get(id=user_id)

    context = {
        'current_user_id' : request.session['user_id'],
        'user_to_delete'  : user.id,
        'user'            : user
    }

    return render(request, 'userDashboard/warning.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    if request.method == 'POST':
        try:#if no user with this email, flash error msg.
            current_user = User.objects.get(email = request.POST['email'])

            #if entered hashed input password does not match the user's hashed password
            #flash error msg.
            if bcrypt.checkpw(request.POST['password'].encode(), current_user.password.encode()):
                request.session['user_id'] = current_user.id

                # check if user has shoppingcart
                # try:
                #     shoppingCart = ShoppingCart.objects.get(id=current_user.id)
                # except:
                #     shoppingCart = ShoppingCart(user=current_user)
                #     shoppingCart.save()

                # checks if current user is admin
                if current_user.user_level == 9:
                    request.session['isAdmin'] = True
                    return redirect('/dashboard')
                else:
                    request.session['isAdmin'] = False
                    return redirect('/products')
            else:
                messages.error(request, 'Your Login information does not match our database. Please try again.')

        except:
            messages.error(request, 'Your Login information does not match our database. Please try again.')
    return redirect('/signin')

def admin_create_user(request):
    if request.method == 'POST':

        # validate our form data
        errors = User.objects.user_validator(request.POST)

        # populate messages with errors if true
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/users/new')
        else:
        # if no errors
            try:
                # check email if it already exists in the database.
                check_email = User.objects.get(email = request.POST['email'])
                messages.error(request, 'This email already exists.')
                return redirect('/users/new')
            except:
                # hash password
                hash_it = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

                # if first user in data base assign admin user level
                check_users = User.objects.all()
                if len(check_users) > 0:
                    user_level = 1
                else:
                    user_level = 9

                # insert user into database
                user = User(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'],password=hash_it,user_level=user_level)
                user.save()
                messages.success(request, 'You have successfully added user.')
    return redirect('/dashboard/admin')

def add_user(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('/')

    if request.session['isAdmin'] == False:
        return redirect('/dashboard')

    context = {
        'current_user_id' : request.session['user_id'],
    }

    return render(request, 'user_app/add_user.html', context)

def update_user(request, user_id):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/users/edit/'+str(user_id))
        else:
            user = User.objects.get(id=user_id)
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            messages.success(request,'Successfully updated User information.')

    return redirect('/dashboard/users/'+request.session['userpage'])

def update_password(request, user_id):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/users/edit/'+str(user_id))
        else:
            user = User.objects.get(id=user_id)
            hash_it = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user.password = hash_it
            user.save()
            # messages.success(request,'Successfully updated password.')

    return redirect('/users/edit/'+str(user_id))

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('/dashboard/admin')

# def userdashboard(request, page):
#     userCount = User.objects.count()
#     getUsers =  User.objects.all()[(int(page)-1)*10:((int(page)-1)*10)+10]
#     newArr=[]
#     for i in range(1,int(math.ceil((userCount/10.0)) + 1)):
#         newArr.append(i)

#     context={
#         'users': User.objects.all(), 'numPages':newArr
#     }
#     return render(request, 'userDashboard/userdash.html', context)

def prodDashboardload(request, page):
    request.session['prodpage']=page
    productCount=Product.objects.all().count()
    allProducts=Product.objects.all()[(int(page)-1)*10:((int(page)-1)*10)+10]

    newArr=[]
    for i in range(1,int(math.ceil((productCount/10.0)) + 1)):
        newArr.append(i)
    
    context={
        'products':allProducts, 'numPages':newArr, 'categories':Category.objects.all()
    }
    return render(request, 'userDashboard/prodtable.html', context)

def userDashboardload(request, page):
    request.session['userpage']=page
    userCount=User.objects.all().count()
    allUsers=User.objects.all()[(int(page)-1)*10:((int(page)-1)*10)+10]

    newArr=[]
    for i in range(1,int(math.ceil((userCount/10.0)) + 1)):
        newArr.append(i)
    
    context={
        'users':allUsers, 'numPages':newArr
    }
    return render(request, 'userDashboard/usertable.html', context)

def userDashboard(request):
    context={
        'users':User.objects.all()#, 'numPages':newArr
    }
    return render(request, 'userDashboard/userdash.html', context)

def delete_user(request, id):
    User.objects.get(id=id).delete()
    return redirect('/dashboard/users/'+request.session['userpage'])