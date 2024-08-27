"""Конфигурация для pytest."""
import pytest
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test.client import Client
from django.utils import timezone
from django.conf import settings

from news.models import News, Comment


User = get_user_model()


@pytest.fixture
def author(db):
    """Создание пользователя автора."""
    return User.objects.create(username='Лев Толстой')


@pytest.fixture
def reader(db):
    """Создание пользователя читателя."""
    return User.objects.create(username='Читатель простой')


@pytest.fixture
def news(db):
    """Создание новости."""
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def comment(news, author):
    """Создание комментария."""
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def client_with_author_logged_in(author):
    """Клиент с авторизацией для автора."""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def client_with_reader_logged_in(reader):
    """Клиент с авторизацией для читателя."""
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news_list(db):
    """Создание списка новостей."""
    today = datetime.today()
    new_list = [
        News(
            title=f'Новость {index}',
            text='Просто текст',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(new_list)


@pytest.fixture
def single_news(db):
    """Создание одной новости."""
    return News.objects.create(title='Тестовая новость', text='Просто текст')


@pytest.fixture
def comments(single_news, author):
    """Создание нескольких комментариев."""
    now = timezone.now()
    comments = []
    for index in range(10):
        comment = Comment.objects.create(
            news=single_news,
            author=author,
            text=f'Текст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
        comments.append(comment)
    return comments
