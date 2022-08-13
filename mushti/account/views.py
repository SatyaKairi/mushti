import imp
from multiprocessing import AuthenticationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.forms import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models.query_utils import Q

from .forms import *

# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        user = authenticate(
            username=username,
            password=password
        )
        if user :
            login(request=request,user= user)
            url = request.GET.get('next')
            if url:
                return redirect(url)
            else:
                return redirect('project:list_view')
        else:
            form.add_error(field=None, error= AuthenticationError("Incorrect username or password"))


    context ={
        'form':form
    }
    return render(request,'account/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('project:list_view')


def profile_create_view(request):
    form = ProfileCreateForm(request.POST or None)
    user = request.user
    qs = Profile.objects.filter(user_id = user.id)
    # qs = Profile.objects.get(user_id = user.id)
    # print(qs.first_name)
    if qs:
        print('redirecting')
        return redirect ('detail_view')
        # return render(request,'account/detail.html',{'object':qs})

    if form.is_valid():
        form.save(commit=False)
        profile = form.instance
        profile.user =request.user
        # profile.save()
        form.save()
        redirect('detail_view')

    context ={
        'form':form
    }
    return render(request,'account/create_profile.html',context)

def user_create_view(request):
    form = UserCreateForm(request.POST or None)
    if request.POST.get('password') != request.POST.get('password1'):
            form.add_error(field=None,error=ValidationError('Password should match.'))
    if form.is_valid():
        
        form.save(commit=False)

        user = form.instance
        user.is_staff = True
        print (form.cleaned_data['password'])
        user.set_password(form.cleaned_data['password'])
        form.save()
        login(request=request,user= user)
        return redirect("create_view")


    
    context ={
        'form':form

    }
    return render(request, 'account/create.html',context)

def profile_detail_view(request, *args, **kwargs):
    id = request.user.id
    profile= get_object_or_404(klass=Profile, user_id = id)
    print(profile)
    context = {
        'object' : profile
    }
    return render(request, 'account/detail.html', context= context)



    
# Create your views here.
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset/email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'aryabhatta_ics@outlook.com',
                                  [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid header found.')
                    return redirect("../../password_reset/done/")
    password_reset_form = PasswordResetForm()
    context = {
        'form': password_reset_form
    }
    return render(request=request, template_name="password_reset/password_reset_request.html", context=context)


