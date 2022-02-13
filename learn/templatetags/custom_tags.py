from django import template
import math

#Django template custom math filters
#Ref : https://code.djangoproject.com/ticket/361
register = template.Library()

def rating(value, arg):
    "Divides the value by the arg"
    if value == None:
        return "NA"
    div = int(value) / int(arg)
    return math.trunc(div * 100)

def null_checker(value):
    if value == None:
        return "NA"

register.filter('rating', rating)
register.filter('null_checker', null_checker)