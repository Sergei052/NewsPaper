from django.views.generic import DetailView, ListView,CreateView,UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Author
from django_filters.views import FilterView
from .forms import PostForm, PostFilterSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


class NewsListView(ListView):
    """Список публикаций с типом «новость»."""

    model = Post
    ordering= '-created_at'
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(postType=Post.NEWS)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_num = page_obj.number

        # Показываем ближайшие страницы (макс 5)
        if paginator.num_pages <= 5:
            context['page_range'] = paginator.page_range
        else:
            if page_num <= 3:
                context['page_range'] = range(1, 4)
            elif page_num >= paginator.num_pages - 2:
                context['page_range'] = range(paginator.num_pages - 2, paginator.num_pages + 1)
            else:
                context['page_range'] = range(page_num - 1, page_num + 2)

        context['show_first_page'] = page_num > 3
        context['show_last_page'] = page_num < paginator.num_pages - 2
        context['total_pages'] = paginator.num_pages

        return context

class NewsDetailView(DetailView):
    """Страница одной новости."""

    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'

    def get_queryset(self):
        return super().get_queryset().filter(postType=Post.NEWS)

class NewsSearchView(FilterView):
    """Поиск и фильтрация новостей."""

    model = Post
    filterset_class = PostFilterSet
    template_name = 'news/news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(postType=Post.NEWS).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_num = page_obj.number

        if paginator.num_pages <= 5:
            context['page_range'] = paginator.page_range
        else:
            if page_num <= 3:
                context['page_range'] = range(1, 4)
            elif page_num >= paginator.num_pages - 2:
                context['page_range'] = range(paginator.num_pages - 2, paginator.num_pages + 1)
            else:
                context['page_range'] = range(page_num - 1, page_num + 2)

        context['show_first_page'] = page_num > 3
        context['show_last_page'] = page_num < paginator.num_pages - 2
        context['total_pages'] = paginator.num_pages

        return context

class NewsCreateView(LoginRequiredMixin,CreateView):
    """Создание новости."""

    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:list')
    login_url = 'admin:login'

    def form_valid(self, form):
        # Получаем автора текущего пользователя
        author = get_object_or_404(Author, authorUser=self.request.user)
        form.instance.postAuthor = author
        form.instance.postType = Post.NEWS
        return super().form_valid(form)
class NewsEditView(LoginRequiredMixin, UpdateView):
    """Редактирование новости."""

    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news:list')
    login_url = 'admin:login'

    def get_queryset(self):
        # Пользователь может редактировать только свои новости
        return super().get_queryset().filter(postType=Post.NEWS, postAuthor__authorUser=self.request.user)

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление новости."""

    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:list')
    login_url = 'admin:login'
    def get_queryset(self):
        # Пользователь может удалять только свои новости
        return super().get_queryset().filter(postType=Post.NEWS, postAuthor__authorUser=self.request.user)

class ArticleListView(ListView):
    """Список статей с постраничным выводом"""
    model = Post
    ordering = '-created_at'
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(postType=Post.ARTICLE)

    def get_contest_date(self,**kwargs):
        context= super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_num = page_obj.number

        if paginator.num_pages <= 5:
            context['page_range'] = paginator.page_range
        else:
            if page_num <= 3:
                context['page_range'] = range(1, 4)
            elif page_num >= paginator.num_pages - 2:
                context['page_range'] = range(paginator.num_pages - 2, paginator.num_pages + 1)
            else:
                context['page_range'] = range(page_num - 1, page_num + 2)

        context['show_first_page'] = page_num > 3
        context['show_last_page'] = page_num < paginator.num_pages - 2
        context['total_pages'] = paginator.num_pages

        return context

class ArticleDetailView(DetailView):
    """Страница одной статьи"""
    model = Post
    template_name = "articles/article_detail.html"
    context_object_name = 'article'

    def get_queryset(self):
        return super().get_queryset().filter(postType=Post.ARTICLE)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Создание статьи."""

    model = Post
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles:list')
    login_url = 'admin:login'
    def form_valid(self, form):
        author = get_object_or_404(Author, authorUser=self.request.user)
        form.instance.postAuthor = author
        form.instance.postType = Post.ARTICLE
        return super().form_valid(form)


class ArticleEditView(LoginRequiredMixin, UpdateView):
    """Редактирование статьи."""

    model = Post
    form_class = PostForm
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles:list')
    login_url = 'admin:login'
    def get_queryset(self):
        return super().get_queryset().filter(postType=Post.ARTICLE, postAuthor__authorUser=self.request.user)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление статьи."""

    model = Post
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles:list')
    login_url = 'admin:login'
    def get_queryset(self):
        return super().get_queryset().filter(postType=Post.ARTICLE, postAuthor__authorUser=self.request.user)
