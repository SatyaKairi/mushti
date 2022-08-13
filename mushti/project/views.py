from django.http import Http404

from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.db.models import Q
from .forms import *
# Create your views here.

def project_list_view(request,*args, **kwargs):
    q= request.GET.get('q')
    qs = Project.objects.get_all_active_projects()
    if not q is None:
        search_param =  Q(name__icontains =q )| Q( description__icontains = q)
        qs = qs.filter(search_param)
    context ={
        'object_list': qs
        
    }
    if request.htmx:
        return render(request,'project/pertial/list.html',context)    
    return render(request,'project/list.html',context)

def project_deactivate_view(request):
    if request.POST:
        id = request.POST.get('project_id')
        project = Project.objects.get(id=id)
        project.is_active = False
        project.modified_by = request.user
        project.save()
        return redirect('project:list_view')

def project_detail_view(request,id,*args, **kwargs):
    project = get_object_or_404(Project,id=id,is_active = True)
    contrib_list=project.get_active_contributions()
    description_images = project.get_active_description_images()
    context ={
        'object':project,
        'contrib_list':contrib_list,
        'descriptions' : description_images
    }
    if request.htmx:
        return render(request,'project/pertial/detail.html',context)
    
    return render(request,'project/detail.html',context)



def project_create_update_view(request,*args, **kwargs):
    project=None
    msg = "Create Project"
    project_id = kwargs.get('id')
    if not project_id is None:
        project = Project.objects.get(id=project_id)
        msg = "Update Project"
        form = ProjectCreateForm(request.POST or None, instance=project,)
    else:
        form = ProjectCreateForm(request.POST or None)
        form2 = ProjectImageCreateForm(request.POST or None)
    # form = ProjectCreateForm(request.POST or None, request.FILES)
    if request.POST:
        form = ProjectCreateForm(request.POST or None, request.FILES)
        form2 = ProjectImageCreateForm(request.POST or None, request.FILES)
        
        if all([form.is_valid(), form2.is_valid()]):
            
            project =form.instance
            project.user = request.user
            project_image = form2.instance
            form.save()
           
            project_image.project_id = project.id
            print('project id'+ str(project.id))
            project_image.save()
            form2.instance.save()



            
            return redirect (form.instance.get_detail_url())             
    context = {
            'form':form,
            'form2': form2,
            'object':project,
            'msg':msg

        }      
    return render(request,'project/create.html',context)   




def project_contribution_create_view(request,*args, **kwargs):

    if request.POST:
        form = ProjectContributionCreateForm(request.POST or None)

        if form.is_valid():
            project_id = request.POST.get('project_id')

            project_contrib = form.instance
            project_contrib.project = Project.objects.get(id=project_id)
            project_contrib.contributor = request.user
            
            form.save()
            return redirect ('project:detail_view',project_contrib.project.id )
            
        else:
            return redirect ('project:detail_view', request.POST.get('project_id') )
    else:
        raise Http404


def project_image_create_view(request,*args, **kwargs):

    form = ProjectImageCreateForm(request.POST or None)
    context = {
        'form': form
    }
    return render(request, 'project/pertial/create_description_image.html', context)


