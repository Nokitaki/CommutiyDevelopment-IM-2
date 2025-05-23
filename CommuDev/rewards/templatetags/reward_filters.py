# rewards/templatetags/reward_filters.py
from django import template

register = template.Library()

@register.filter(name='div')
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0