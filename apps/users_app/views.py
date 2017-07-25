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
from django.contrib import messages
import bcrypt

def index(request):

    return render(request, 'users_app/index.html')

def dashboard(request):

    users = User.objects.all()

    current_user = User.objects.get(id=request.session['user_id'])


    context = {
        'current_user_id' : request.session['user_id'],
        'users'           : users,
        'isAdmin'         : request.session['isAdmin']
    }

    return render(request, '/users_app/dashboard.html', context)

def login(request):
    if request.method == 'POST':
        try:
            get_email = User.objects.get(email = request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), get_email.password.encode()):
                request.session['user_id'] = get_email.id

                current_user = User.objects.get(id=request.session['user_id'])

                return redirect('/dashboard')

        except:
            messages.error(request, 'Your information is incorrect. Please try again.')
    return redirect('/index')

def create_user(request):
    #---------------------------------------------
    #------------- make a new user ---------------
    #---------------------------------------------
    if request.method == 'POST':

        # validate all form data
        errors = User.objects.user_validator(request.POST)

        # populate messages with errors or specifics if true
        if len(errors):
            for error in errors:
                messages.error(request, error)
            return redirect('/index')
        else:
        # if errors FREE
            try:
                # does email already exist in database
                check_email = User.objects.get(email = request.POST['email'])
                messages.error(request, 'Please try another email input.')

                return redirect('/index')

            except:
                # hash password
                hash_it = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

                # insert user into database
                user = User(user_name=request.POST['first_name'], alias=request.POST['last_name'],email=request.POST['email'],password=hash_it)
                user.save()
                messages.success(request, 'You have successfully registered')
    return redirect('/index')


def user(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You are not logged in.')
<<<<<<< HEAD
        return redirect('/users')

    user = User.objects.get(id=user_id)

=======
        return redirect('/index')

    user = User.objects.get(id=user_id)


>>>>>>> master
    context = {
        'user' : user,
    }
    return render(request, 'users_app/user.html', context)

def logout(request):
    request.session.clear()
<<<<<<< HEAD
    return redirect('/users')
=======
    return redirect('/index')

def signin(request):
    if request.method == 'POST':
        try:
            get_email = User.objects.get(email = request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), get_email.password.encode()):
                request.session['user_id'] = get_email.id

                current_user = User.objects.get(id=request.session['user_id'])

                return redirect('/user')

        except:
            messages.error(request, 'Your information is incorrect. Please try again.')
    return redirect('/signin')
>>>>>>> master
