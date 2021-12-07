from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import HttpResponseRedirect
from .models import *
from .forms import *


def search_index(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(Q(title__icontains=searched) | Q(content__icontains=searched))
        context = {'searched': searched, 'posts':posts}
        return render(request, 'weblog/search_index.html', context=context)
    
    else:
        return render(request, 'weblog/search_index.html')

def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # print("i clicked the other form button :(((((")

    if 'create_comment' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(slug=slug)
            comment.owner = request.user
            comment.save()
            form.save()
            messages.info(request, f"Comment created successfully.", extra_tags='success')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    elif 'comment_like' in request.POST:
        comment = get_object_or_404(Comment, id=request.POST.get('comment_like'))
        print(f'comment_like - id={comment.id}')
        comment.like.add(request.user)
    elif 'comment_dislike' in request.POST:
        comment = get_object_or_404(Comment, id=request.POST.get('comment_dislike'))
        print(f'comment_dislike - id={comment.id}')
        comment.dislike.add(request.user)

    elif 'post_like' in request.POST:
        print(f'post_like - id:{post.id}')
        post.like.add(request.user)
    elif 'post_dislike' in request.POST:
        print(f'post_dislike - id:{post.id}')
        post.dislike.add(request.user)
    
    return redirect(reverse('weblog:post_detail', args=[slug]))


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
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm()
    total_likes = post.total_likes()
    total_dislikes = post.total_dislikes()
    context = {'post': post, 'form': form, 'total_likes':total_likes, 'total_dislikes':total_dislikes}
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
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
            # return redirect(reverse('weblog:post_list'))

# TODO: Handle Comment Like - Multiple Form Mechanism
def comment_like(request, id):
    comment = get_object_or_404(Comment, id=id)

    print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHhh")
    print(id)
    print(request.POST)
    if 'comment_like' in request.POST:
        comment.like.add(request.user)
    elif 'comment_dislike' in request.POST:
        comment.dislike.add(request.user)
    
    # redirect to the previous page :D
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


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

# password reset: https://ordinarycoders.com/blog/article/django-password-reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.', extra_tags="success")
                    return redirect ("weblog:home")
            messages.error(request, 'An invalid email has been entered.', extra_tags="danger")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

# contact form: https://ordinarycoders.com/blog/article/build-a-django-contact-form-with-email-backend
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry" 
            body = {
            'first_name': form.cleaned_data['first_name'], 
            'last_name': form.cleaned_data['last_name'], 
            'email': form.cleaned_data['email_address'], 
            'message':form.cleaned_data['message'], 
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
                messages.success(request, 'An Email has been sent to your inbox.', extra_tags="success")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            
            return redirect ("weblog:home")

    form = ContactForm()
    return render(request, "weblog/contact.html", {'form':form})