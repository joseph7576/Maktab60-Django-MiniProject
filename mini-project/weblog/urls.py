from django.urls import path
from .views import *

app_name = 'weblog'
urlpatterns = [
    path('', test_index, name='test'),
    path('posts/', post_list, name='post_list'),
    path("post/<slug:slug>", post_detail, name="post_detail"),
    path("categories/", CategoryList.as_view(), name="category_list"),
    path("cateogry/<int:pk>", CategoryDetail.as_view(), name="category_detail"),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]

