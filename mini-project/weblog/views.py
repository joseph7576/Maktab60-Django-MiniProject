from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

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

