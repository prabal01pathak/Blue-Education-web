from django.shortcuts import render

# courses list
def courses_list(request):
    return render(request,'courses/courses_list.html',{})
