from django.shortcuts import render, HttpResponse, redirect
from .models import Title, StudentData, Math, Chemistry, Physics,Biology,Agriculture
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import TestForm,FormFilter
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
        if model.marking != 0:
            mark = model.marking
        else:
            mark += marking
        right += 1
    elif choice == None or choice == "":
        mark += 0
    else:
        if model.minus_marking != 0:
            mark -= model.minus_marking
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

    # paper time details 
    endtime = title.end_time 
    server_end = title.end_time+timezone.timedelta(minutes=1)
    time_now = timezone.now()

    if time > server_end and title.is_live:
        context = {
            'title': 'Exam End',
            'data': '<h2>Exam Ended</h2>'
        }
        return render(request,'result.html',context)


    # get data of every subject from database
    models = {}
    models_list = {}


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

    total_remaining_time = (endtime - title.scheduled_time).seconds
    remaining_minutes = int(total_remaining_time/60)
    context = {
        'title': title,
        'models_list': models_list,
        "end_time": endtime,
        "subject_detail":subject_detail,
        "nowTime": time,
        'remaining_time': remaining_minutes,
        'total_time':remaining_minutes,
    }


    if title.is_live:
        time_delay = ((time_now - title.scheduled_time).seconds)/60
        total_remaining_minutes = int(remaining_minutes - time_delay)
        context['remaining_time']=total_remaining_minutes
    #time of exam and submission

    if request.method == "POST":
        #get submitted time.
        time = timezone.now()
        if time >server_end and title.is_live:
            context = {
                'title': 'Exam End',
                'data': '<h2>Exam Ended</h2>'
            }
            return render(request,'result.html',context)
        try:
            # get database if exist and set marks and attempts
            student = StudentData.objects.get(user=request.user, paper=title)
        except StudentData.DoesNotExist:
            # create database if not exist
            student = StudentData.objects.create(
                user=request.user, paper=title,submitted_at=time) 

        if student.attempts >= 1 and title.is_live:
            title = 'resubmission'
            context = {
                'title':title,
                'data':"<h2>You have already submitted</h2>"
            }
            return render(request,'result.html',context)
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

'''
title = Title.objects.get(id=1)
for i in range(0,200):
    Agriculture.objects.create(paper_title=title,description="sldfjsldjfsldjfsdjfsdfjsldjfsdjfdsf" )
    print(i)

    '''

def home(requests):
    titles = Title.objects.filter(is_live=True,hidden=False)
    now_time = timezone.now()
    for title in titles:
        end_time = title.end_time
        remove_live = title.remove_live_minutes
        remove_live_time = end_time + timezone.timedelta(minutes=remove_live)
        if now_time > remove_live_time:
            title.is_live = False
            title.save()
    total_title = Title.objects.filter(hidden=False)
    form = FormFilter()
    context = {
        'titles': total_title,
        'form': form,
    }
    if requests.method=="POST":
        form = FormFilter(requests.POST)
        filter_type = requests.POST['exam_type']
        total_title = Title.objects.filter(exam_type=filter_type)
        context['titles'] = total_title
        context['form'] = form
        return render(requests,'home.html',context)
    return render(requests, 'home.html', context)
