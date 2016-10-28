from django.template import Library
register = Library()

@register.inclusion_tag('arduino/controls.html')
def insert_arduino_controls():
    return {}
