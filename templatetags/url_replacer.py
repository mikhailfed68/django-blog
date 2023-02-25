from django import template

register = template.Library()


# This tag was created to be used to keep the pagination state
# with search query, when visitor steps through
# each of the individual pages
@register.simple_tag(takes_context=True)
def replace_param(context, **kwargs):
    """
    Replaces the parameters with new values 
    in query string and removes those
    that have no values.
    """
    querydict = context["request"].GET.copy()
    for param, value in kwargs.items():
        querydict[param] = value

    for param in [param for param, value in querydict.items() if not value]:
        del querydict[param]

    return querydict.urlencode()
