
from email.policy import default
from unicodedata import category
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.

class ProjectManager(models.Manager):
    def get_all_active_projects(self):
        return Project.objects.filter(is_active = True)
    

class Project(models.Model):
    cat_choices = (
        ('Art','Art'),
        ( 'Culture' ,'Culture'),
        ('Social', 'Social'),
        ('Creativity','Creativity'),
        ('Education','Education'),
        ('Film','Film'),
        ('Food & Crafts', 'Food & Crafts'),
        ('Game', 'Game'),
        ('Music','Music'),
        ('Publishing','Publishing'),
        ('Others','Others')

    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    project_image = models.ImageField(upload_to = 'images/')
    category = models.CharField(max_length=50, choices=cat_choices,default='Others')
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank = True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank = True, related_name="modified_project_user")
    is_active = models.BooleanField(default=True)
    objects=ProjectManager()

    def get_active_contributions(self):
        rs = self.projectcontribution_set.filter(is_active = True)
        return rs

    def get_active_description_images(self):
        rs = self.projectimages_set.filter(is_active = True)
        return rs

    def get_funded_amount(self):
        amount =self.get_active_contributions().aggregate(total=models.Sum('amount'))
        funded_amount =amount.get('total',0)
        if funded_amount==None:
            funded_amount=0
        return round(funded_amount,2)

    def get_funded_percentage(self):
        amount = self.get_funded_amount()
        return round( amount/self.budget * 100,0)
    # Urls
    def get_detail_url(self,**kwargs):
        return reverse ('project:detail_view', kwargs={'id' :self.id})
    def get_update_url(self,**kwargs):
        return reverse ('project:update_view', kwargs={'id' :self.id})
    def get_deactivate_url(self,**kwargs):
        return reverse ('project:deactivate_view')
    def get_contrib_url(self):
        return reverse('project:contrib_create_view')
    def get_description_image_url(self):
        return reverse('project:description_image_create_view')

    def __str__(self):
        return self.name
    

class ProjectContribution(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    contributor = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank = True)
    comments = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank = True, related_name="modified_user")
    is_active = models.BooleanField(default=True)


class ProjectImages(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'project_description/')
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now = True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name='updated_by')
    is_active = models.BooleanField(default=True)

    