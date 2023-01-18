from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def replace_param(context, **kwargs):
    querydict = context['request'].GET.copy()
    for param, value in kwargs.items():
        querydict[param] = value

    for param in [param for param, value in querydict.items() if not value]:
        del querydict[param]

    return querydict.urlencode()
