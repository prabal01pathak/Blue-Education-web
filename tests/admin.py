from django.contrib import admin
from .models import  Title,StudentData,Math,Chemistry,Physics


admin.site.register(Title)
admin.site.register(Math)
admin.site.register(Chemistry)
admin.site.register(Physics)
admin.site.register(StudentData)
