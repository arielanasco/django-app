from django import template
import math

#Django template custom math filters
#Ref : https://code.djangoproject.com/ticket/361
register = template.Library()

def rating(value, arg):
    "Divides the value by the arg"
    div = int(value) / int(arg)
    return math.trunc(div * 100)

register.filter('rating', rating)