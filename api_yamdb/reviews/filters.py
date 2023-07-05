from django_filters import FilterSet, CharFilter

from reviews.models import Title


class TitleFilterSet(FilterSet):
    '''Фильтр для произведений'''

    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
