from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import SlugField

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Post Owner")
    title = models.CharField("Title Post", max_length=30)
    content = models.TextField()
    category = models.ManyToManyField('Category')
    created = models.DateField(auto_now_add=True, null=True)
    slug = models.SlugField(max_length=40, unique=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f'Comment of Post:{self.post}'
    
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField('Title Category', max_length=30)

    def __str__(self):
        return self.title
    