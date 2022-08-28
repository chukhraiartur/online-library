from django import template
from books.models import *

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories(filter=None):
    ''' A simple tag that returns a collection of categories '''
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('books/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    ''' An inclusion tag that creates the template and returns it '''
    if not sort:
        categories = Category.objects.all()
    else:
        categories = Category.objects.order_by(sort)
    
    return {'categories': categories, 'cat_selected': cat_selected}