from django import template
from ..models import Category

register = template.Library()

BAD_WRDS = ['редиска', 'попка']

@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Это не строка')

    for w in BAD_WRDS:
        value = value.replace(w[1:], '*' * (len(w)-1))
        return value

@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()

