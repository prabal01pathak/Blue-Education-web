from django import template
from tests.views import get_subjects_list

register = template.Library()


@register.filter
def subjects_list(value):
    subjects = get_subjects_list(value)
    return subjects


@register.filter(name='index')
def index(value, arg):
    return value[arg]['choices']


@register.filter(name='index_value')
def index_value(value, arg):
    return value[arg-1]


@register.filter(name='filter_subject')
def filter_subject(value, arg):
    print(value)
    print(arg)
    return value[arg]
