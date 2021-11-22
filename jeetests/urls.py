"""jeetests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from home.views import create
from django.conf.urls.static import static
from django.conf import settings
from JEE.views import upload_img

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', upload_img, name='image-upload'),
    path('', include('tests.urls')),
    path('', include('courses.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('tinymce', include('tinymce.urls')),
    path('user_auth/', include('user_auth.urls')),
    re_path(r'^create/page-(?P<year>[0-9]{4})', create),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
