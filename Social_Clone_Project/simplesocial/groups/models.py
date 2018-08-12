from django.db import models
# GROUPS
 # Create your models here.
from django.urls import reverse

from django.utils.text import slugify
# import misaka
#misaka- link embedding
from django.contrib.auth import get_user_model

User = get_user_model()
from django import template
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,blank=True,default=True)
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = self.description
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']

class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name= 'memberships',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_group',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')