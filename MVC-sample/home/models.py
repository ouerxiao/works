from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

STATUS = (
    ('True', 'True'),
    ('False', 'False'),
)

class Setting(models.Model):
    title = models.CharField(max_length=32)
    keywords = models.CharField(max_length=100)
    description = models.CharField(max_length=225)
    company = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    smtpserver = models.CharField(blank=True, max_length=20)
    smtpemail = models.CharField(blank=True, max_length=20)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='icon/')
    facebook = models.CharField(blank=True, max_length=50)
    istagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'home_setting'

class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )

    name = models.CharField(blank=True, max_length=20, verbose_name="name")
    email = models.CharField(blank=True, max_length=50, verbose_name="email")
    subject = models.CharField(blank=True, max_length=50,verbose_name="subject" )
    message = models.CharField(blank=True, max_length=225, verbose_name="message")
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'home_contactmessage'

class FAQ(models.Model):

    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )

    postnumber = models.IntegerField()
    question =  models.CharField(max_length=200)
    answer = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'home_faq'