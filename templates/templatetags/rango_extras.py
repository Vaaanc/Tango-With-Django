from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat':cat}

@register.inclusion_tag('rango/cats.html')
def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if cat_list and max_results > 0:
        if cat_list.count() > max_results:
            cat_list = cat_list[:max_results]

    return cat_list
