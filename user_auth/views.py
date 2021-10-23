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
from .forms import UserCreate,PasswordChangeForm,UserProfile
from django.shortcuts import render, redirect,reverse
from .models import UserExtraData
from django.contrib.auth.decorators import login_required
import math
import random
import string
from tests.models import StudentData,Title
from tests.views import get_object
import json

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
        print(form.is_valid())
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('Email')
            user_data.mobile_number = form.cleaned_data.get('mobile_no')
            user_data.gender = form.cleaned_data.get("gender")
            user.save()
            user_data.save()
            print('done')
            return redirect(request.path)
    return render(request, 'registration/profile.html', {'form': form, 'user_data': user_data})

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
            try: 
                User.objects.get(email=email)
                return render(request, 'registration/register.html', {'form': form, 'error': 'Email already exists'})
            except User.DoesNotExist:
                User.objects.create(username=username,password=password, email=email, first_name=first_name, last_name=last_name)
                user_status = User.objects.get(username=username)
                user_status.active = False
                user_status.save()
            last_name = form.cleaned_data.get('last_name')
            user = User.objects.get(username=username)
            UserExtraData.objects.create(user=user, mobile_number=mobile_no, accept_terms=accept_terms)
            print(username, raw_password, email, mobile_no, first_name, last_name)
            return redirect('/')
        return render(request, 'registration/register.html', {'form': form})
    return render(request, 'registration/register.html', {'form': form})

def login_user(request):
    print(dir(request))
    if request.user.is_authenticated:
        print(request.path)
        return redirect('/')
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        raw_password = request.POST['password']
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            print(request.path)
            try:
                print(request.path)
                path = request.get_full_path_info()
                next_path = path.split('=')[1]
                print(next_path)
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
    print(otp)
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
    print(data)
    return render(request,'registration/dashboard.html',context)


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
            model = get_object(title, subject)
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