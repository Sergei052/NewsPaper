from django import forms
from django.db.models import Q
from django_filters import CharFilter, DateFilter, FilterSet

from .models import Post


class PostFilterSet(FilterSet):
    """Фильтр для поиска новостей и статей."""

    postTitle = CharFilter(
        field_name='postTitle',
        lookup_expr='icontains',
        label='По названию',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    author_name = CharFilter(
        method='filter_author',
        label='По автору',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    created_at_after = DateFilter(
        field_name='postDate',
        lookup_expr='date__gte',
        label='Позже (дата)',
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d',
        ),
    )

    class Meta:
        model = Post
        fields = []

    def filter_author(self, queryset, name, value):
        user = 'postAuthor__authorUser__'
        return queryset.filter(
            Q(**{f'{user}username__icontains': value})
            | Q(**{f'{user}first_name__icontains': value})
            | Q(**{f'{user}last_name__icontains': value})
        )


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования новостей и статей."""

    class Meta:
        model = Post
        fields = ['postTitle', 'postText', 'postCategory']
        labels = {
            'postTitle': 'Заголовок',
            'postText': 'Текст публикации',
            'postCategory': 'Категория',
        }
        widgets = {
            'postTitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок...',
            }),
            'postText': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Введите текст...',
            }),
            'postCategory': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input',
            }),
        }