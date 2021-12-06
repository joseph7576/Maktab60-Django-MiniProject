from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *

def post_create(request):
    if request.method == 'POST':
        print(request.FILES)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            form.save_m2m()
            messages.info(request, f"Post created successfully.", extra_tags='success')
            return redirect(reverse('weblog:dashboard'))
    else:
        form = PostForm()

    return render(request, 'weblog/post_create.html',{'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        messages.info(request, f"Post updated successfully.", extra_tags='success')
        return redirect(reverse('weblog:post_list'))

    return render(request, 'weblog/post_edit.html', {'form': form })

def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        post.delete()
        messages.info(request, f"Post deleted successfully.", extra_tags='success')
        return redirect(reverse('weblog:post_list'))
    
    return render(request, 'weblog/post_delete.html', {'post': post})

def post_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'weblog/post_list.html', context=context)

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    form = CommentForm()
    context = {'post': post, 'form': form}
    return render(request, 'weblog/post_detail.html', context=context)

def create_comment(request):
    if request.method == 'POST':
        post_slug = request.POST.get('post_slug')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(slug=post_slug)
            comment.owner = request.user
            comment.save()
            form.save()
            messages.info(request, f"Comment created successfully.", extra_tags='success')
            return redirect(reverse('weblog:post_list'))


class CategoryList(ListView):
    model = Category

class CategoryDetail(DetailView):
    model = Category

class TagList(ListView):
    model = Tag

class TagDetail(DetailView):
    model = Tag

def dashboard_view(request):
    user = request.user
    posts = Post.objects.filter(owner=user)
    context = {'user': user, 'posts': posts}
    return render(request, 'login/dashboard.html', context=context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.", extra_tags='success')
                return redirect(reverse('weblog:dashboard'))
            else:
                messages.error(request,"Invalid username or password.", extra_tags='danger')
        else:
            messages.error(request,"Invalid username or password.", extra_tags='danger')

    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.",  extra_tags='success')
    return redirect(reverse('weblog:home'))
    
def register_view(request):

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
            messages.info(request, f"You have successfully registered as {username}.", extra_tags='success')
            return redirect(reverse('weblog:login'))
    
    return render(request, 'login/register.html', {'form':form})


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        category.delete()
        messages.info(request, f"Category deleted successfully.", extra_tags='success')
        return redirect(reverse('weblog:category_list'))
    
    return render(request, 'weblog/category_delete.html', {'category': category})

def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None,instance=category)
    
    if form.is_valid():
        form.save()
        messages.info(request, f"Category updated successfully.", extra_tags='success')
        return redirect(reverse('weblog:category_list'))

    return render(request, 'weblog/category_edit.html', {'form': form })

def create_category(request):
    form = CategoryForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.info(request, f"Category created successfully.", extra_tags='success')
        return redirect(reverse('weblog:category_list'))

    return render(request, 'weblog/category_create.html', {'form': form})


def delete_tag(request, id):
    tag = get_object_or_404(Tag, id=id)

    if request.method == 'POST':
        tag.delete()
        messages.info(request, f"Tag deleted successfully.", extra_tags='success')
        return redirect(reverse('weblog:tag_list'))
    
    return render(request, 'weblog/tag_delete.html', {'tag': tag})

def edit_tag(request, id):
    tag = get_object_or_404(Tag, id=id)
    form = TagForm(request.POST or None,instance=tag)
    
    if form.is_valid():
        form.save()
        messages.info(request, f"Tag updated successfully.", extra_tags='success')
        return redirect(reverse('weblog:tag_list'))

    return render(request, 'weblog/tag_edit.html', {'form': form })

def create_tag(request):
    form = TagForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.info(request, f"Tag created successfully.", extra_tags='success')
        return redirect(reverse('weblog:tag_list'))

    return render(request, 'weblog/tag_create.html', {'form': form})
