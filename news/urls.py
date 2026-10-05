from django.urls import path

from .views import (
    NewsDetailView, NewsListView, NewsSearchView,
    NewsCreateView,NewsEditView, NewsDeleteView,
    ArticleListView,ArticleDetailView,ArticleCreateView,
    ArticleEditView,ArticleDeleteView
)


app_name = 'news'

urlpatterns = [
    # Новости
    path('', NewsListView.as_view(), name='list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='detail'),
    path('search/', NewsSearchView.as_view(), name='search'),
    path('create/', NewsCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', NewsEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='delete'),

    # Статьи
    path('articles/', ArticleListView.as_view(), name='articles_list'),
    path('articles/<int:pk>/',ArticleDetailView.as_view(), name='articles_detail' ),
    path('articles/create/', ArticleCreateView.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArticleEditView.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='articles_delete'),
]


