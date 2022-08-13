from dataclasses import fields
from django import forms
from django.forms.models import inlineformset_factory
from .models import Project, ProjectContribution, ProjectImages

class ProjectContributionCreateForm(forms.ModelForm):
    
    class Meta:
        model = ProjectContribution
        fields =['amount','comments']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                {
            'placeholder': f'{str(field)}',
            'class': 'form-control'
            }  
        )



class ProjectImageCreateForm(forms.ModelForm):
    
    class Meta:
        model = ProjectImages
        fields =['image','description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widgets={
            'description':forms.Textarea(
                attrs={'rows':2,
                'placeholder':'Image Description'
                
                }
            )
        }
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                {
            'placeholder': f'{str(field)}',
            'class': 'form-control'
            }  
        ) 


ProjectImageFormSet = inlineformset_factory(
    Project,
    ProjectImages,
    ProjectImageCreateForm,
    can_delete=False,
    min_num= 3,
    extra= 0
    
)
class ProjectCreateForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['name','description','budget', 'category', 'project_image']
        widgets={
            'description':forms.Textarea(
                attrs={'rows':2,
                'placeholder':'description'
                
                }
            )
        }
        
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update(
                {
            'placeholder': f'{str(field)}',
            'class': 'form-control'
            }
                
        )
        



            

    
    
