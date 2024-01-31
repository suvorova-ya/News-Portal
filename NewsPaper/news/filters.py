from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter
from .models import Category
from django.forms import TimeInput


class PostFilter(FilterSet):
    category = ModelChoiceFilter(queryset=Category.objects.all(), empty_label='Все категории')
    title = CharFilter(lookup_expr='icontains', label='Заголовок')
    data = DateTimeFilter(field_name='date_creation', lookup_expr='gt', label="Дата",
                               widget=TimeInput(format='%Y-%m-%d', attrs={'type': 'datetime-local'},),)

