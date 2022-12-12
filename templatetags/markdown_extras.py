from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
import bleach
from bleach_allowlist import markdown_attrs, markdown_tags

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    """
    Принимает размеченный murkdown текст и возвращает
    очищенную html разметку с разрешенными элементами для murkdown.
    Неразрешенные элементы будут экранированы.
    """
    return bleach.clean(
        md.markdown(value, extensions=['markdown.extensions.fenced_code']),
        markdown_tags,
        markdown_attrs,
    )
