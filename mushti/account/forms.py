
from django import forms
from django.contrib.auth.models import User

from account.models import Profile
class LoginForm(forms.Form):
    error_css_class="bg-primary"
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200,widget=forms.PasswordInput)
    
    class Meta():
        
        model = User
        fields = ['username','password']
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({
                'class':'form-control',
                'placeholder': f'{str(field)}'.title().replace('_',' ')
            }
            )



class ProfileCreateForm(forms.ModelForm):
    
    class Meta():
        model = Profile
        fields=['first_name','last_name','phone_no','address']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({
                'class':'form-control',
                'placeholder': f'{str(field)}'.title().replace('_',' ')
            }
            )


class UserCreateForm(forms.ModelForm):
    error_css_class ="alert alert-warning"
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
    password1 = forms.CharField(label="Re enter password", max_length=200,   widget=forms.PasswordInput(attrs={
        'placeholder':'confirm password'
    }))
    class Meta():
        model = User
        fields =['username','password']
    
    def __init__(self,*args, **kwargs):

        super().__init__(*args,**kwargs)
        
        for field in self.fields:
            self.fields[str(field)].widget.attrs.update({
                'class':'form-control',
                'placeholder': f'{str(field).title()}',
                'label' :''
                }
                
            )
            self.fields[str(field)].label=''
        self.fields['password1'].widget.attrs.update({
                'placeholder':'Confirm password'
                }
                
            )