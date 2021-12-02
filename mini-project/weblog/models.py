from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import random, string
from django.db.models.signals import pre_save

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
    title = models.CharField("Title Post", max_length=30)
    content = models.TextField()
    category = models.ManyToManyField('Category')
    created = models.DateField(auto_now_add=True, null=True)
    slug = models.SlugField(max_length=40, unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

def pre_save_receiver(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_slug_generator(instance) 

pre_save.connect(pre_save_receiver, sender = Post) 

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
    