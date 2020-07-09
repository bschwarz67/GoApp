from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
def split(value):
	return list(value)


register.filter('split', split)
