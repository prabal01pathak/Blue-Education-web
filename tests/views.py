from django.shortcuts import render, HttpResponse, redirect
from .models import Title, StudentData, Math, Chemistry, Physics,Biology
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# , UserChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import TestForm
from django.utils import timezone
import json
from django.apps import apps
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import tzlocal


# get time of database
def get_time():
    import datetime
    now = datetime.datetime.now()
    html = "Time: %s" % now
    return html


counter = 0


def check_answers(choice, model, marking, minus_marking):
    # check type of input question
    mark = 0
    right = 0
    if model.type == "write":
        answer = model.option1
    else:
        answer = model.answer

    # manipulate the marks based on answer given by student
    if choice != None and choice.lower() == answer.lower():
        mark += marking
        right += 1
    elif choice == None or choice == "":
        mark += 0
    else:
        mark -= minus_marking
    return mark, right


def get_object(title, subject):
    models = apps.get_models()

    try:
        for model in models:
            models_name = str(model.__name__)
            if models_name == subject:
                return model.objects.filter(paper_title=title)

    except ObjectDoesNotExist:
        return []


def split_model_name(name):
    name = name.split('_')
    last_name = name[1]
    return last_name


def get_posted_datas(request, models_list, marking, minus_marking):
    marking = float(marking)
    minus_marking = float(minus_marking)
    choices = []
    rights = 0
    marks = 0
    datas = {}
    for key in models_list.keys():
        model_data = models_list[key]['model_name']
        name = models_list[key]['name']
        i = 0
        for data in model_data:
            choice = request.POST.get(f"option_{name}{i+1}")
            choices.append(choice)
            model = data
            mark, right = check_answers(choice, model, marking, minus_marking)
            marks += mark
            rights += right
            i += 1
            datas[name] = {
                'marks': marks,
                'rights': rights,
                'choices': choices,
            }

        marks = 0
        rights = 0
        choices = []
    return datas


def get_marks_and_rights(data):
    marks = 0
    rights = 0
    for subjects, values in data.items():
        mark = values['marks']
        right = values['rights']
        marks += mark
        rights += right
    return marks, rights


def calculate_rank(title,user):
    students = StudentData.objects.filter(paper=title).order_by('-marks') # get all students of this title and order by marks 
    i =0
    for user_ in students:
        user_.rank = i+1
        user_.save()
        i += 1
    student = StudentData.objects.get(paper=title,user=user)
    return student.rank

# exam page


@login_required(login_url="user_auth:login")
def index(request, title_id):
    time = timezone.now()
    # get paper titles from database
    title = Title.objects.filter(id=title_id, hidden=False)

    # select first if multiple titles
    title = title[0]


    # get data of every subject from database
    models = {}
    models_list = {}

    # paper time details 
    end_hour = float(title.end_hours)
    endtime = title.scheduled_time + timezone.timedelta(hours=end_hour)

    #Append every new model subjects in subjects list.
    subjects = ['Math', 'Physics', 'Chemistry', 'Biology', 'Agriculture']
    total_subject = 0
    total_questions = 0
    subject_wise_total_questions = 0
    subjects_name = ""
    for subject in subjects:
        model = get_object(title, subject)
        if model != None and len(model) > 0:
            models_list[f"model_{subject}"] = {
                'model_name': model,
                'name': subject
            }
            total_questions += len(model)
            total_subject +=1
            subject_wise_total_questions += len(model)
            subjects_name += f"{total_subject+2}. {model[0].name()} \t has Total of {subject_wise_total_questions} questions.<br>"
            subject_wise_total_questions =0

    #subject details 
    total_marks = total_questions * float(title.marking_scheme)
    total_subject_marks = total_marks / total_subject
    #    "total_subject_marks": total_subject_marks,
    every_subject_questions = total_questions / total_subject
    subject_detail = {
        "total_marks": int(total_marks),
        "every_subject_questions":int(every_subject_questions),
        "total_subject_marks": int(total_subject_marks),
        'subjects_name': subjects_name,
    }

    context = {
        'title': title,
        'models_list': models_list,
        "total_time": end_hour,
        "end_time": endtime,
        "subject_detail":subject_detail,
        "nowTime": time,
    }



    #time of exam and submission

    if request.method == "POST":
        #get submitted time.
        time = timezone.now()
        try:
            # get database if exist and set marks and attempts
            student = StudentData.objects.get(user=request.user, paper=title)
        except StudentData.DoesNotExist:
            # create database if not exist
            student = StudentData.objects.create(
                user=request.user, paper=title,submitted_at=time) 

        if student.attempts >= 1 and title.is_live:
            return HttpResponse("you have already submitted")
        if time >endtime and title.is_live:
            return HttpResponse("Exam ended")
        # get student total posted data
        exam_data = get_posted_datas(
            request, models_list, title.marking_scheme, title.minus_marking_scheme)

        total_marks, total_rights = get_marks_and_rights(exam_data)

        # caculate student rank

        student.exam_data = exam_data
        student.attempts += 1
        student.submitted_at = timezone.now()
        student.marks = total_marks
        student.save()
        rank = calculate_rank(title,request.user)
        print("rank: ",rank)
        # change data to show in result page.
        for choices in exam_data:
            context[choices] = exam_data[choices]
        context['student'] = student
        context['exam_data'] = exam_data
        context['total_marks'] = total_marks
        context['total_rights'] = total_rights
        context['rank'] = rank
        return render(request, 'index.html', context)
    return render(request, 'index.html', context)

# home page

# home view for user
#
title = Title.objects.get(id=2)
for i in range(0,200):
    break
    Chemistry.objects.create(paper_title=title,description="sldfjsldjfsldjfsdjfsdfjsldjfsdjfdsf" )
    print(i)


def home(requests):
    titles = Title.objects.filter(hidden=False)
    print(timezone.now())
    context = {
        'titles': titles,
    }
    return render(requests, 'home.html', context)
