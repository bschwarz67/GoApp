from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
def split(value):
	return list(value)

def numberRange(number):
	return range(number)

register.filter('split', split)
register.filter('numberRange', numberRange)
