from django import template
import re

register = template.Library()

_TAGS = [('редис','р****'), ('Редиска','Р******')]

@register.filter(name='length')
def currency(value):

   return f'{len(value)} '

@register.filter(name='censor')
def currency(value):
   if type(value)==str:
      for pattern, repl in _TAGS:
        value = re.sub(pattern, repl, value)
   return value 

@register.filter(name='post_id')
def currency(value):
   return f'/news/{value}'

@register.filter(name='update')
def currency(value):
   if value.item!='ART':
      return f'/news/{value.id}/edit/'
   else:
      return f'/news/articles/{value.id}/edit/'

@register.filter(name='delete')
def currency(value):
   if value.item!='ART':
      return f'/news/{value.id}/delete/'
   else:
      return f'/news/articles/{value.id}/delete/'