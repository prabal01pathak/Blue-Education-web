from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import (
    login, 
    authenticate,
    logout, 
    update_session_auth_hash,
)
from django.contrib.auth.hashers import make_password,check_password 
from django.contrib.auth.models import User
from django.apps import apps
from .forms import UserCreate,PasswordChangeForm,UserProfile,PasswordResetForm

from django.shortcuts import render, redirect,reverse
from .models import *
from django.contrib.auth.decorators import login_required
import math
import random
import string
from tests.models import StudentData,Title
from tests.views import get_object
import json
from tests.extra_utils import send_simple_mail,code_generator

@login_required(login_url="user_auth:login")
def profile(request):
    user = request.user
    try:
        user_data = UserExtraData.objects.get(user=user)
    except UserExtraData.DoesNotExist:
        user_data = user
    form = UserProfile({'first_name':user.first_name, 'last_name':user.last_name, 'username':user.username, 'Email':user.email,'mobile_no':user_data.mobile_number}) 
    if request.method=="POST":
        form = UserProfile(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('Email')
            user_data.mobile_number = form.cleaned_data.get('mobile_no')
            user_data.gender = form.cleaned_data.get("gender")
            user.first_name=first_name
            user.email = email

            user.save()
            user_data.save()
            return redirect(request.path)
    return render(request, 'registration/profile.html', {'form': form, 'user_data': user_data})

#change Password
def change_password(request):
    #Reset password form
    form = PasswordResetForm()
    context = {
            'form':form,
            }
    otp = request.session['otp']
    username = request.session['username']
    if request.method=="POST":
        form = PasswordResetForm(request.POST)
        user_otp = request.POST['OTP']
        if user_otp == otp:
            if form.is_valid():
                raw_password = request.POST['new_password']
                hash_password = make_password(raw_password)
                print(hash_password)
                user = User.objects.get(username=username)
                user.set_password(raw_password)
                user.save()
                update_session_auth_hash(request, request.user)
                return redirect(reverse("user_auth:login"))
            context['form']=form
            return render(request,'password_change.html',context)
        context['message']="Please enter right otp"
        return render(request,'password_change.html',context)
    return render(request,'password_change.html',context)


def verify_otp(request):
    if request.user.is_authenticated:
        return redirect("/")
    username = request.session['username']
    otp = request.session['otp']
    if request.method=="POST":
        user_otp = request.POST['verify_otp']
        print(user_otp)
        print(otp)
        if otp==user_otp:
            user = User.objects.get(username=username)
            user.is_active=True
            user.save()
            return redirect(reverse("user_auth:login"))
        return render(request,'verify_otp.html',{'message':True,'error':'Please enter right OTP'})
    return render(request,'verify_otp.html',{'message':False})

# reset password view
def reset_password(request):
    if request.method=="POST":
        # get username and serach for it 
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            request.session['username']=username
            request.session['email']=user.email
            otp=code_generator()
            request.session['otp']=otp
            request.session['name']=user.first_name
            request.session['purpose']="Reset Password"
            send_simple_mail({'otp':otp,
                              'name':user.first_name,
                              'email':user.email,
                              'purpose':"Reset Password",
                          })
            return redirect(reverse("user_auth:change-pass"))
        except User.DoesNotExist:
            #return if user not exist
            return render(request,'reset_password.html',{"message":True,"error":"Please enter correct username"})
    return render(request,'reset_password.html',{})

def resend_otp(request,some):
    if request.user.is_authenticated:
        return redirect("/")
    otp = code_generator()
    request.session['otp']=otp
    username=request.session['username']
    user = User.objects.get(username=username)
    email = user.email
    first_name = user.first_name
    send_simple_mail({'otp':otp,
                      'name':first_name,
                      'email':email,
                      'purpose':"registration",
                      })
    request.session.set_expiry(180)
    print(request.path)
    if some=="change":
        form = PasswordResetForm()
        return render(request,'password_change.html',{'form':form,'otp':True})
    return render(request,'verify_otp.html',{'otp':True})

@login_required(login_url="user_auth:login")
def edit_profile(request):
    user = request.user
    user_data = UserExtraData.objects.get(user=user)
    if request.method == 'POST':
        user_data.mobile_number = request.POST['mobile_number']
        user_data.accept_terms = request.POST['accept_terms']
        user_data.save()
        return redirect('/')
    return render(request, 'registration/edit_profile.html', {'user_data': user_data})

@login_required(login_url="user_auth:login")
def password_change(request):
    form  = PasswordChangeForm()
    if request.method=="POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            old_password = form.cleaned_data['old_password']
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('/')
            error = "wrong old password "
            return render(request,'registration/password_change.html',{'form':form,'error':error}) 
    return render(request, 'registration/password_change.html', {'form': form})

def create_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserCreate()
    if request.method == 'POST':
        form = UserCreate(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('Email')
            mobile_no = form.cleaned_data.get('mobile_no')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            accept_terms = form.cleaned_data.get('accept_terms')
            password = make_password(raw_password)
            #get user if exist 
            try: 
                User.objects.get(email=email)
                return render(request, 'registration/register.html', {'form': form, 'error': 'Email already exists'})
            except User.DoesNotExist:
                User.objects.create(username=username,password=password, email=email, first_name=first_name, last_name=last_name)
                user_status = User.objects.get(username=username)
                user_status.is_active=False
                user_status.save()

            # generate otp
            otp = code_generator()
            #set otp,and requested path in request variable
            print(dir(request))
            request.session['otp']=otp
            request.session['call_path']=request.path
            request.session['username']=username
            request.session['email']=email
            request.session["purpose"]="registration"
            send_simple_mail({'otp':otp,
                              'name':first_name,
                              'email':email,
                              'purpose':"registration",
                              })

            # set expiry date of session in browser side
            request.session.set_expiry(180)
            print(request.session.get_expiry_date())
            print(code_generator)
            last_name = form.cleaned_data.get('last_name')
            user = User.objects.get(username=username)
            UserExtraData.objects.create(user=user, mobile_number=mobile_no, accept_terms=accept_terms)
            return redirect(reverse("user_auth:verify"))
        return render(request, 'registration/register.html', {'form': form})
    return render(request, 'registration/register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        raw_password = request.POST['password']
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            try:
                path = request.get_full_path_info()
                next_path = path.split('=')[1]
            except:
                next_path = '/'
            return redirect(next_path)
        else:
            return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid username or password'})
    return render(request, 'registration/login.html', {'form': form})
def logout_user(request):
    logout(request)
    return redirect('/') 

def password_reset(request):
    email_otp = generate_otp()
    mobile_otp = generate_otp()
    return render(request, 'registration/password_reset.html')

def generate_otp():
    strings = string.ascii_letters + string.digits
    otp = ''.join(random.choice(strings) for i in range(8))
    return otp 
@login_required(login_url="user_auth:login")
def dashboard(request):
    user = request.user
    data = StudentData.objects.filter(user=user)
    if len(data) >0:
        context = {
            'data':data
        }
    else: 
        context = {}
    return render(request,'registration/dashboard.html',context)


@login_required(login_url="user_auth:login")
def view_paper(request,title_id):
    user = request.user 
    paper = Title.objects.filter(id=title_id)
    title = paper[0]
    models = {}
    models_list = {}
    try:
        student_data = StudentData.objects.get(user=user,paper=title)
        json_data  = student_data.exam_data
        exam_data = eval(json_data)
        subject_list = []
        total_marks = 0
        total_rights = 0
        for keys in exam_data.keys():
            subject_list.append(keys)
            total_marks += exam_data[keys]['marks']
            total_rights += exam_data[keys]['rights']

        for subject in subject_list:
            model,model_name = get_object(title, subject)
            if model != None and len(model) > 0:
                models_list[f"model_{subject}"] = {
                    'model_name': model,
                    'name': subject
                }
        context ={
            'exam_data':exam_data,
            'models_list':models_list,
            'total_marks':total_marks,
            'total_rights':total_rights,
            'rank':student_data.rank,
            'title':title,
        } 
    except:
        context = {'question_error':'No data found'}

    return render(request,'paper/paper.html',context)
