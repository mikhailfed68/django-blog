from django import template

register = template.Library()


# This tag was created to be used to move through the resulting list
# of objects, keeping the parameters of the previous search query
@register.simple_tag(takes_context=True)
def replace_param(context, **kwargs):
    """Replaces with new parameters passed and clears parameters."""
    querydict = context["request"].GET.copy()
    for param, value in kwargs.items():
        querydict[param] = value

    for param in [param for param, value in querydict.items() if not value]:
        del querydict[param]

    return querydict.urlencode()
