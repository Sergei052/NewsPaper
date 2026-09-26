from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Author, Post

from .templatetags.news_filters import censor

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

class CensorFilterTests(TestCase):
    def test_censor_replaces_forbidden_words(self):
        result = censor('Это плохой и ужасный текст')

        self.assertEqual(
            result,
            'Это п****й и у****ый текст',
        )

    def test_censor_works_without_case_sensitivity(self):
        self.assertEqual(censor('ПЛОХО'), 'П****')
        self.assertEqual(censor('Плохо'), 'П****')

    def test_censor_handles_empty_value(self):
        self.assertEqual(censor(''), '')
        self.assertIsNone(censor(None))