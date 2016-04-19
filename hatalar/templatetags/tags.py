from django import template
from django_jinja.builtins.filters import slugify

register = template.Library()

@register.simple_tag
def slugyap(gelen):
    return slugify(gelen)