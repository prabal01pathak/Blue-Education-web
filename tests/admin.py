from django.contrib import admin
from .models import  Title,StudentData,Math,Physics,Biology,Agriculture,Chemistry


admin.site.register(Title)
admin.site.register(Math)
admin.site.register(Chemistry)
admin.site.register(Physics)
admin.site.register(Biology)
admin.site.register(Agriculture)
admin.site.register(StudentData)
