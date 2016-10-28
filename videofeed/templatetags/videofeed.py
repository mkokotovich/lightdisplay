from django.template import Library
register = Library()

@register.inclusion_tag('videofeed/feed.html')
def insert_videofeed():
    return {}
