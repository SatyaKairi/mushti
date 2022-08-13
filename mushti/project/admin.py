from django.contrib import admin
from .models import *


# Register your models here.
class ProjectContributionInline(admin.TabularInline):
    model=ProjectContribution
    extra = 0

class ProjectImagesInline(admin.TabularInline):
    model= ProjectImages
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines=[
        ProjectImagesInline,
        ProjectContributionInline
    ]

admin.site.register(Project,ProjectAdmin)