from django import template
import math
from django.conf import settings
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

def admin_email_checker(value):
    if value == None:
        return settings.ADMINS[0][1]

register.filter('rating', rating)
register.filter('null_checker', null_checker)
register.filter('admin_email_checker', admin_email_checker)