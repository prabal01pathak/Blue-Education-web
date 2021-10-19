from django import template

register = template.Library()

@register.filter(name='index')
def index(value,arg):
    return value[arg]['choices']
@register.filter(name='index_value')
def index_value(value,arg):
    return value[arg-1]