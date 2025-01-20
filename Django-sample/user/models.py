from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.utils.html import mark_safe


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='username')
    phone = models.CharField(blank=True, max_length=20, verbose_name='phone')
    address = models.CharField(blank=True, max_length=150, verbose_name='address')
    city = models.CharField(blank=True, max_length=20, verbose_name='city')
    country = models.CharField(blank=True, max_length=20, verbose_name='country')
    avatar = models.ImageField(blank=True, upload_to='avatar/', verbose_name='avatar', )

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + '[' + self.user.username + ']'

    def avatar_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.avatar.url))
    avatar_tag.short_description = 'avatar'

    class Meta:
        db_table = 'user_userprofile'
