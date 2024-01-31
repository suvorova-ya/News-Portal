from django import template


register = template.Library()

BAD_WRDS = ['редиска', 'попка']

@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Это не строка')

    for w in BAD_WRDS:
        value = value.replace(w[1:], '*' * (len(w)-1))
        return value


