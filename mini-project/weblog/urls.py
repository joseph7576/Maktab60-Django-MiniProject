from django.urls import path
from .views import *

app_name = 'weblog'
urlpatterns = [
    path('', test_index, name='test'),
    
    path('posts/', post_list, name='post_list'),
    path("post/<slug:slug>", post_detail, name="post_detail"),

    path('tags/', TagList.as_view(), name='tag_list'),
    path("tag/<int:pk>", TagDetail.as_view(), name="tag_detail"),
    path("tag_delete/<int:id>", delete_tag, name="tag_delete"),
    path('tag_edit/<int:id>', edit_tag, name='tag_edit'),
    path('tag_create/', create_tag, name='tag_create'),


    path("categories/", CategoryList.as_view(), name="category_list"),
    path("category/<int:pk>", CategoryDetail.as_view(), name="category_detail"),
    path("category_delete/<int:id>", delete_category, name="category_delete"),
    path('category_edit/<int:id>', edit_category, name='category_edit'),
    path('category_create/', create_category, name='category_create'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]

