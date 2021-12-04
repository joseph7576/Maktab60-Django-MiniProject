from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import random, string
from django.db.models.signals import pre_save

User = get_user_model()

# https://studygyaan.com/django/how-to-create-a-unique-slug-in-django
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 
def unique_slug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.title) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return unique_slug_generator(instance, new_slug = new_slug) 
    return slug 

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Post Owner")
    title = models.CharField("Post Title", max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='images', null=True)
    category = models.ManyToManyField('Category')
    created = models.DateField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)
    tag = models.ManyToManyField('Tag')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

# TODO: search about pre_save & Django Signals
def pre_save_receiver(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_slug_generator(instance) 
pre_save.connect(pre_save_receiver, sender = Post) 

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Comment Owner", null=True)
    text = models.TextField()
    like = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Comment of User:{self.owner} on Post:{self.post}'
    
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Category Name', max_length=30, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(max_length=30)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name