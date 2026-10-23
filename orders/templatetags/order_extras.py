from django import template

register = template.Library()

@register.filter
def edge(value):
    return format(value.normalize(), 'f') if value else ''