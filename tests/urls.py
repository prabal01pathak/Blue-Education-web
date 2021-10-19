from django.urls import path
from .views import index,home

app_name = 'jeetests'
urlpatterns = [
        path('', home, name='home'),
        path("jee/paper/<int:title_id>/", index, name='index'),
]
