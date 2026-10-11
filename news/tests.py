from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Author, Category, Post
from .templatetags.news_filters import censor


class NewsViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('editor')
        author = Author.objects.create(authorUser=self.user)
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

    def test_search_finds_news_by_title(self):
        response = self.client.get(reverse('news:search'), {'postTitle': 'дня'})

        self.assertContains(response, 'Новость дня')

    def test_search_shows_message_when_nothing_found(self):
        response = self.client.get(reverse('news:search'), {'postTitle': 'нет такой'})

        self.assertContains(response, 'ничего не найдено')

    def test_article_create_redirects_to_articles_list(self):
        self.client.force_login(self.user)
        category = Category.objects.create(categoryName='Наука')

        response = self.client.post(reverse('news:articles_create'), {
            'postTitle': 'Новая статья',
            'postText': 'Текст статьи',
            'postCategory': [category.pk],
        })

        self.assertRedirects(response, reverse('news:articles_list'))
        self.assertTrue(
            Post.objects.filter(postTitle='Новая статья', postType=Post.ARTICLE).exists()
        )

    def test_create_requires_login(self):
        response = self.client.get(reverse('news:create'))

        self.assertEqual(response.status_code, 302)


class CensorFilterTests(TestCase):
    def test_censor_replaces_forbidden_words(self):
        result = censor('Это плохой и ужасный текст')

        self.assertEqual(result, 'Это п***** и у****** текст')

    def test_censor_works_without_case_sensitivity(self):
        self.assertEqual(censor('ПЛОХО'), 'П****')
        self.assertEqual(censor('Плохо'), 'П****')

    def test_censor_handles_empty_value(self):
        self.assertEqual(censor(''), '')
        self.assertIsNone(censor(None))