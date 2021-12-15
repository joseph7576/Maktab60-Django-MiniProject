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


### post model
# custom manager for post
class PublishedPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PU')

class DraftPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='DR')

class Post(models.Model):
    
    PU = 'PU'
    DR = 'DR'

    STATUS_CHOICE = [
        (PU, 'Published'),
        (DR, 'Draft')
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Post Owner")
    title = models.CharField("Post Title", max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='images', null=True)
    category = models.ManyToManyField('Category')
    created = models.DateField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name='post_like')
    dislike = models.ManyToManyField(User, related_name='post_dislike')
    tag = models.ManyToManyField('Tag')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICE,
        default=DR
    )

    # config managers
    objects = models.Manager()
    published = PublishedPostsManager() # views - Line 70 & 80
    draft = DraftPostsManager() # not used in this project

    def total_likes(self):
        return self.like.count()

    def total_dislikes(self):
        return self.dislike.count()

    def __str__(self):
        return self.title

### create unique slug for post
# TODO search about pre_save & Django Signals
def pre_save_receiver(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_slug_generator(instance) 
pre_save.connect(pre_save_receiver, sender = Post) 


# comment model
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Comment Owner", null=True)
    text = models.TextField()
    like = models.ManyToManyField(User, related_name='comment_like')
    dislike = models.ManyToManyField(User, related_name='comment_dislike')
    updated_on = models.DateTimeField(auto_now=True, null=True)

    @property
    def total_likes(self):
        return self.like.count()

    @property
    def total_dislikes(self):
        return self.dislike.count()

    def __str__(self):
        return f'Comment of User:{self.owner} on Post:{self.post}'


# category model
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField('Category Name', max_length=30, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


# tag model   
class Tag(models.Model):
    name = models.CharField(max_length=30)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name