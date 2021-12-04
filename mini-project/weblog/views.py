from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *

def test_index(request):
    return render(request, 'weblog/index.html')

def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'weblog/post_list.html', context=context)

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    context = {'post': post}
    return render(request, 'weblog/post_detail.html', context=context)

class CategoryList(ListView):
    model = Category

class CategoryDetail(DetailView):
    model = Category

class TagList(ListView):
    model = Tag

def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('weblog:test'))

    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})
    
def register_form(request):
    form = RegisterForm(None or request.POST)
    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(first_name=first_name,
                                       last_name=last_name,
                                       username=username,
                                       email=email,
                                       password=password)
            return redirect(reverse('weblog:login'))
    
    return render(request, 'login/register.html', {'form':form})