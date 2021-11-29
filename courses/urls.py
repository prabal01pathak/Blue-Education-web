from django.urls import re_path,path
from .views import courses_list

app_name = 'courses'
urlpatterns = [
    path('courses_list/',courses_list,name='courses-list'),

]
