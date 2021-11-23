from django.shortcuts import render
from .forms import NormalForm

# Create your views here.
def create(request):
    form = NormalForm()
    return render(request,'change_form.html',{'form':form})
