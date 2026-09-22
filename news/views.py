from django.views.generic import DetailView, ListView

from .models import Post


class NewsListView(ListView):
    """Список публикаций с типом «новость»."""

    model = Post
    ordering= '-created_at'
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    ordering = ['-postDate']

    def get_queryset(self):
        return super().get_queryset().filter(postType=Post.NEWS)


class NewsDetailView(DetailView):
    """Страница одной новости."""

    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().filter(postType=Post.NEWS)
