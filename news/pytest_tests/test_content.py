"""Тесты для контента."""
import pytest

from django.urls import reverse
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, news_list):
    """Проверка количества новостей на главной странице."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_list):
    """Проверка сортировки новостей на главной странице."""
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_order(client, single_news, comments):
    """Проверка сортировки комментариев."""
    url = reverse('news:detail', args=(single_news.id,))
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize(
    'client_fixture, expected_form_present',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('client_with_author_logged_in'), True)
    )
)
@pytest.mark.django_db
def test_comment_form_visibility(
    client_fixture, expected_form_present, single_news
):
    """Проверка видимости формы добавления комментария."""
    url = reverse('news:detail', args=(single_news.id,))
    response = client_fixture.get(url)
    form_present = 'form' in response.context
    assert form_present == expected_form_present

    if form_present:
        assert isinstance(response.context['form'], CommentForm)
