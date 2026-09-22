from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Author, Post


class NewsViewsTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('editor')
        author = Author.objects.create(authorUser=user)
        self.news = Post.objects.create(
            postAuthor=author,
            postType=Post.NEWS,
            postTitle='Новость дня',
            postText='Текст новости',
        )
        Post.objects.create(
            postAuthor=author,
            postType=Post.ARTICLE,
            postTitle='Статья',
            postText='Текст статьи',
        )

    def test_news_list_shows_only_news(self):
        response = self.client.get(reverse('news:list'))

        self.assertContains(response, 'Новость дня')
        self.assertNotContains(response, 'Статья')
        self.assertTemplateUsed(response, 'news/news_list.html')

    def test_news_detail_is_available_for_news(self):
        response = self.client.get(reverse('news:detail', args=[self.news.pk]))

        self.assertContains(response, 'Текст новости')
        self.assertTemplateUsed(response, 'news/news_detail.html')
