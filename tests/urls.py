from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 
from .views import index,home,show_title,get_subject,add_questions,edit_question,show_assign_or_delete,edit_title,add_title,terms

app_name = 'jeetests'
urlpatterns = [
        path('', home, name='home'),
        path("paper/<int:title_id>/", index, name='index'),
        path("show/paper/", show_title, name='show-title'),
        path("add/paper/", add_title, name='add-title'),
        path("edit/paper/<int:title_id>", edit_title, name='edit-title'),
        path("subjects/<int:title_id>/", get_subject, name='get-subject'),
        path("show/questions/<str:model>/<int:title_id>/", show_assign_or_delete, name='show-question'),
        path("add/questions/<str:model>/<int:title_id>/", add_questions, name='add-question'),
        path("edit/question/<int:question_id>/<str:model>/<int:title_id>/", edit_question, name='edit-question'),
        path("terms" , terms,name="terms"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
