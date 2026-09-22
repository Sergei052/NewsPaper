from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone


class Author(models.Model):
    """Дополнительные данные пользователя, который публикует материалы."""

    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.IntegerField(default=0)

    def update_rating(self):
        """Пересчитать рейтинг автора по его публикациям и комментариям."""
        posts_rating = self.post_set.aggregate(total=Sum('postRating'))['total'] or 0
        comments_rating = self.authorUser.comment_set.aggregate(
            total=Sum('commentRating')
        )['total'] or 0
        comments_to_posts_rating = Comment.objects.filter(
            commentPost__postAuthor=self
        ).aggregate(total=Sum('commentRating'))['total'] or 0

        self.authorRating = posts_rating * 3 + comments_rating + comments_to_posts_rating
        self.save(update_fields=['authorRating'])


class Category(models.Model):
    """Тематическая категория публикаций."""

    categoryName = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    )

    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    postType = models.CharField(max_length=2, choices=POST_TYPES)
    postDate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    postTitle = models.CharField(max_length=128)
    postText = models.TextField()
    postRating = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255, default='')
    text = models.TextField(default='', blank=True)
    def __str__(self):
        return f'{self.title}'

    def like(self):
        self.postRating += 1
        self.save(update_fields=['postRating'])

    def dislike(self):
        self.postRating -= 1
        self.save(update_fields=['postRating'])

    def preview(self):
        return f'{self.postText[:124]}...'


class PostCategory(models.Model):
    """Связь публикации с её категорией."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """Комментарий пользователя к публикации."""

    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)
    commentRating = models.IntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save(update_fields=['commentRating'])

    def dislike(self):
        self.commentRating -= 1
        self.save(update_fields=['commentRating'])

