from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db import IntegrityError

from .forms import CustomUserCreationForm, CustomUserRegistrationForm
from .models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                hashed_password = make_password(form.cleaned_data['password'])
                new_user = User(username=form.cleaned_data['username'], password=hashed_password)
                new_user.save()
            except IntegrityError as e:
                return render(request, 'multi_user/login_or_register.html', {'form': form, 'error': 'Username already exists'})
                
            login(request, new_user)
            return redirect('index-page')
    else:
        storage = get_messages(request)
        message = ''
        for msg in storage:
            if (msg.tags == "error"):
                message = msg.message

        form = CustomUserRegistrationForm()
        return render(request, 'multi_user/login_or_register.html', {'form': form, 'error': message})


@login_required(login_url='login-or-register-page')
def index(request):

    storage = get_messages(request)
    message = ''
    for msg in storage:
        if (msg.tags == "error"):
            message = msg.message
        elif (msg.tags == "success"):
            message = msg.message

    user = request.user
    access_level = request.user.get_access_level_display()
    form = CustomUserCreationForm()        
    return render(request, 'multi_user/index.html', {'user': user, 'access_level': access_level, 'form': form, 'message': message})


def login_user(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index-page')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login-or-register-page')


def logout_user(request):
    logout(request)
    return redirect('login-or-register-page')


def home(request):
    return redirect('index-page')


@login_required(login_url='login-or-register-page')
@permission_required("multi_user.all_head_office", raise_exception=True)
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                hashed_password = make_password(form.cleaned_data['password'])
                new_user = User(username=form.cleaned_data['username'], password=hashed_password, account_owner=request.user, access_level=form.cleaned_data['access_level'])
                new_user.save()
                messages.success(request, f'User {new_user.username} created successfully')
                return redirect('index-page')
            
            except IntegrityError as e:
                messages.error(request, 'Username already exists')
                return redirect('index-page') 