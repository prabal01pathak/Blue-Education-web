from django.shortcuts import render,HttpResponseRedirect,HttpResponse,reverse,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #, UserChangeForm 
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    form = UserCreationForm()
    context = {
        "form": form,
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_auth:login'))
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', context)



def login_user(request):
    if request.user.is_authenticated:
        return redirect('jeetests:home')
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        print(form.is_valid())
        username =request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print('done')
        if user is not None:
            login(request, user)
            return redirect('/?next=%s' % request.path) 
        else:
            return HttpResponse('Invalid login')
    return render(request, 'login.html',context)

def logout_view(request):
    logout(request)
    return redirect('user_auth:login')