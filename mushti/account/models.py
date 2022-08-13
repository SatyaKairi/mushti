from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField (User, on_delete=models.CASCADE , related_name='profile')
    first_name = models.CharField(max_length=200, null=True,blank=True)
    last_name = models.CharField(max_length=200, null=True,blank=True)
    phone_no = models.CharField(max_length=11, null=True,blank=True)
    address = models.CharField(max_length=200, null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank = True, related_name="modified_profile_user")
    is_active = models.BooleanField(default=True)

    def get_detail_url(self):
        return reverse('profile_detail', kwargs= {'id': self.id})



