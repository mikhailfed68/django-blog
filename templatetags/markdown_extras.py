import bleach
import markdown as md
from bleach_allowlist import markdown_attrs, markdown_tags
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    """
    Accepts murkdown text and returns
    cleaned html markup with allowed elements for murkdown.
    Prohibited elements will be escape.
    """
    return bleach.clean(
        md.markdown(value, extensions=["markdown.extensions.fenced_code"]),
        markdown_tags,
        markdown_attrs,
    )
