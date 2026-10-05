from django import forms
from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post


class PostFilterSet(FilterSet):
    """Фильтр для поиска новостей и статей."""

    postTitle = CharFilter(
        field_name='postTitle',
        lookup_expr='icontains',
        label='По названию'
    )

    author_name = CharFilter(
        field_name='postAuthor__authorUser__first_name',
        lookup_expr='icontains',
        label='По имени автора'
    )

    created_at_after = DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Позже (дата)',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = []


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования новостей и статей."""

    class Meta:
        model = Post
        fields = ['postTitle', 'postText', 'postCategory']
        labels = {
            'postTitle': 'Заголовок',
            'postText': 'Текст публикации',
            'postCategory': 'Категория'
        }
        widgets = {
            'postTitle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок...'
            }),
            'postText': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Введите текст...'
            }),
            'postCategory': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            })
        }