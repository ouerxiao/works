from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from sorl.thumbnail import ImageField, get_thumbnail
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from embed_video.fields import EmbedVideoField

# Create your models here.
STATUS = (
    ('True', 'True'),
    ('False', 'False'),
)

class Category(MPTTModel):
    name = models.CharField(max_length=50)
    keywords = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=30, null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE, db_index=True)
    status = models.CharField(max_length=10, choices=STATUS )

    def __str__(self):
        return str(self.name)

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'id': self.id, 'slug': self.slug})

    def get_ancestors(self):                           
        full_path = []                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
            full_path.reverse()
        return full_path

    class Meta:
        unique_together = ('slug', 'parent')
        db_table = 'blog_category'


STATUS_CHOICES = ( 
   ('draft', 'Draft'), 
   ('published', 'Published'), 
) 

class Post(models.Model):
    title = models.CharField(max_length=50)
    keywords = models.CharField( max_length=50, null=True)
    description = models.CharField( max_length=100, null=True)
    image = models.ImageField(upload_to='images/', )
    symbol = models.ImageField(upload_to="symbols/", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    category = models.ForeignKey('Category',null=True, on_delete=models.CASCADE, related_name='postcategory')
    slug = models.SlugField(null=False, max_length=50, unique=True)
    body = RichTextUploadingField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    bookmark = models.ManyToManyField(User, related_name='bookmark', blank=True)
    
    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if self.image:
            imageTemproary = Image.open(self.image)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize( (800, 500) ) 
            imageTemproaryResized.save(outputIoStream , format='JPEG', quality=60)
            outputIoStream.seek(0)
            self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(Post, self).save(*args, **kwargs)   

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'id':self.id, 'slug': self.slug})

    def get_cat_list(self):
        k = self.category 
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    # method to create fake table, read-only mode
    def image_tag(self):
        return mark_safe('<img src="{}" height="80"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def total_likes(self):
        return self.likes.count()

    class Meta:
        db_table = 'blog_post'  
        ordering = ['-published_at']


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=32, blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    description = RichTextUploadingField(blank=True)
    likes_image = models.ManyToManyField(User, related_name='likes_image', blank=True)
    

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes_image.count()

    def save(self, *args, **kwargs):
        if self.image:
            imageTemproary = Image.open(self.image)
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize( (800, 500) ) 
            imageTemproaryResized.save(outputIoStream , format='JPEG', quality=60)
            outputIoStream.seek(0)
            self.image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        super(PostImage, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('image-detail', kwargs={'id':self.id})


    class Meta:
        db_table = 'blog_postimage'

class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'blog_comment'
 
class Youtube(models.Model):
    video = EmbedVideoField(blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    

    def unicode (self):
        return self.video

    class Meta:
        db_table = 'blog_youtube'