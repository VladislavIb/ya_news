"""Конфигурация для pytest."""
import pytest

from django.contrib.auth import get_user_model
from django.test.client import Client

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
