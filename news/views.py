from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)
from django_filters.views import FilterView

from .forms import PostFilterSet, PostForm
from .models import Author, Post


class PaginationMixin:
    """Добавляет в контекст данные для компактной пагинации (окно из 3 страниц)."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        if paginator is None or page_obj is None:
            return context

        total = paginator.num_pages
        start = min(max(page_obj.number - 1, 1), max(total - 2, 1))
        end = min(start + 2, total)

        context['page_range'] = range(start, end + 1)
        context['show_first_page'] = start > 1
        context['show_last_page'] = end < total
        context['total_pages'] = total
        return context


class PostTypeMixin:
    """Оставляет в выборке только публикации нужного типа (новости или статьи)."""

    post_type = None

    def get_queryset(self):
        return (
            super().get_queryset()
            .filter(postType=self.post_type)
            .select_related('postAuthor__authorUser')
        )


class OwnPostMixin(LoginRequiredMixin, PostTypeMixin):
    """Для правки и удаления: только вошедший пользователь и только свои материалы."""

    def get_queryset(self):
        return super().get_queryset().filter(postAuthor__authorUser=self.request.user)


class PostCreateMixin(LoginRequiredMixin):
    """Общая логика создания: автор берётся из текущего пользователя."""

    model = Post
    form_class = PostForm
    post_type = None

    def form_valid(self, form):
        author, _ = Author.objects.get_or_create(authorUser=self.request.user)
        form.instance.postAuthor = author
        form.instance.postType = self.post_type
        return super().form_valid(form)


# ---------- Новости ----------

class NewsListView(PaginationMixin, PostTypeMixin, ListView):
    """Список публикаций с типом «новость»."""

    model = Post
    post_type = Post.NEWS
    ordering = '-postDate'
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10


class NewsDetailView(PostTypeMixin, DetailView):
    """Страница одной новости."""

    model = Post
    post_type = Post.NEWS
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'


class NewsSearchView(PaginationMixin, PostTypeMixin, FilterView):
    """Поиск и фильтрация новостей."""

    model = Post
    post_type = Post.NEWS
    ordering = '-postDate'
    filterset_class = PostFilterSet
    template_name = 'news/news_search.html'
    context_object_name = 'news'
    paginate_by = 10


class NewsCreateView(PostCreateMixin, CreateView):
    """Создание новости."""

    post_type = Post.NEWS
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:list')


class NewsEditView(OwnPostMixin, UpdateView):
    """Редактирование новости (только своей)."""

    model = Post
    post_type = Post.NEWS
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:list')


class NewsDeleteView(OwnPostMixin, DeleteView):
    """Удаление новости (только своей)."""

    model = Post
    post_type = Post.NEWS
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:list')


# ---------- Статьи ----------

class ArticleListView(PaginationMixin, PostTypeMixin, ListView):
    """Список статей с постраничным выводом."""

    model = Post
    post_type = Post.ARTICLE
    ordering = '-postDate'
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10


class ArticleDetailView(PostTypeMixin, DetailView):
    """Страница одной статьи."""

    model = Post
    post_type = Post.ARTICLE
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'


class ArticleCreateView(PostCreateMixin, CreateView):
    """Создание статьи."""

    post_type = Post.ARTICLE
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('news:articles_list')


class ArticleEditView(OwnPostMixin, UpdateView):
    """Редактирование статьи (только своей)."""

    model = Post
    post_type = Post.ARTICLE
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('news:articles_list')


class ArticleDeleteView(OwnPostMixin, DeleteView):
    """Удаление статьи (только своей)."""

    model = Post
    post_type = Post.ARTICLE
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('news:articles_list')