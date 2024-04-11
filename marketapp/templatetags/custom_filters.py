from django import template
from django.http import QueryDict

register = template.Library()

@register.filter
def removetag(value, param_name):
    query_dict = QueryDict(value, mutable=True)
    query_dict.pop(param_name, None)
    return query_dict.urlencode()