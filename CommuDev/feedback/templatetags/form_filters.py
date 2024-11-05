from django import template
from django.forms.boundfield import BoundField
from django.utils.safestring import SafeString

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Adds a CSS class to a form field widget.
    """
    if isinstance(field, BoundField):
        return field.as_widget(attrs={'class': css_class})
    return field

@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder_text):
    """
    Adds a placeholder to a form field widget.
    """
    if isinstance(field, BoundField):
        return field.as_widget(attrs={'placeholder': placeholder_text})
    return field

@register.filter(name='attr')
def attr(field, attrs):
    """
    Adds multiple attributes to a form field widget.
    """
    if not isinstance(field, BoundField):
        return field
        
    try:
        attrs_dict = dict(item.split(':') for item in attrs.split(','))
        return field.as_widget(attrs=attrs_dict)
    except (ValueError, AttributeError):
        return field