from django.urls import path
from .views import *

app_name = 'weblog'
urlpatterns = [

    # page stuff
    path('', post_list, name='home'), # == post_list
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('search/', search_index, name='search_index'),

    # post stuff
    path('posts/', post_list, name='post_list'),
    path("post/<slug:slug>", post_detail, name="post_detail"),
    path('post_create/', post_create, name='post_create'),
    path('post_edit/<slug:slug>', post_edit, name='post_edit'),
    path('post_delete/<slug:slug>', post_delete, name='post_delete'),
    path('post_stuff/<slug:slug>', post_stuff, name='post_stuff'),

    # category stuff
    path("categories/", CategoryList.as_view(), name="category_list"),
    path("category/<int:pk>", CategoryDetail.as_view(), name="category_detail"),
    path("category_delete/<int:id>", category_delete, name="category_delete"),
    path('category_edit/<int:id>', category_edit, name='category_edit'),
    path('category_create/', category_create, name='category_create'),

    # tag stuff
    path('tags/', TagList.as_view(), name='tag_list'),
    path("tag/<int:pk>", TagDetail.as_view(), name="tag_detail"),
    path("tag_delete/<int:id>", tag_delete, name="tag_delete"),
    path('tag_edit/<int:id>', tag_edit, name='tag_edit'),
    path('tag_create/', tag_create, name='tag_create'),

    # password stuff
    path("password_reset/", password_reset_request, name="password_reset"),
    path('new_password/', new_password, name='new_password'),

    # contact form
    path("contact/", contact, name="contact"),
]

