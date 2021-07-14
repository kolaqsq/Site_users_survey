from django import template

register = template.Library()


@register.filter(name='strip_quotes')
def strip_quotes(quoted_string):
    return quoted_string.replace('\'', '')
