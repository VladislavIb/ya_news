"""Тесты для логики приложения."""
import pytest
from http import HTTPStatus

from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cannot_create_comment(client, single_news, form_data):
    """Анонимный пользователь не может оставлять комментарии."""
    url = reverse('news:detail', args=(single_news.id,))
    client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_user_can_create_comment(
    client_with_author_logged_in, single_news, form_data
):
    """Пользователь может оставлять комментарии."""
    url = reverse('news:detail', args=(single_news.id,))
    response = client_with_author_logged_in.post(url, data=form_data)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == f'{url}#comments'
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == single_news


@pytest.mark.django_db
def test_user_cant_use_bad_words(client_with_author_logged_in, single_news):
    """Пользователь не может использовать запрещенные слова."""
    url = reverse('news:detail', args=(single_news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = client_with_author_logged_in.post(url, data=bad_words_data)
    assert response.status_code == HTTPStatus.OK
    assert 'form' in response.context
    form_error = response.context['form'].errors['text'][0]
    assert form_error == WARNING
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_author_can_delete_comment(
    client_with_author_logged_in, comment
):
    """Автор может удалять свои комментарии."""
    delete_url = reverse('news:delete', args=(comment.id,))
    response = client_with_author_logged_in.delete(delete_url)
    assert response.status_code == HTTPStatus.FOUND
    expected_url = reverse(
        'news:detail', args=(comment.news.id,)
    ) + '#comments'
    assert response.url == expected_url
    comments_count = Comment.objects.count()
    assert comments_count == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(
    client_with_reader_logged_in, comment
):
    """Пользователь не может удалить комментарий другого пользователя."""
    delete_url = reverse('news:delete', args=(comment.id,))
    response = client_with_reader_logged_in.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(
    client_with_reader_logged_in, comment, form_data
):
    """Пользователь не может редактировать комментарий другого пользователя."""
    edit_url = reverse('news:edit', args=(comment.id,))
    response = client_with_reader_logged_in.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'


@pytest.mark.django_db
def test_author_can_edit_comment(
    client_with_author_logged_in, comment, form_data
):
    """Автор может редактировать свои комментарии."""
    edit_url = reverse('news:edit', args=(comment.id,))
    response = client_with_author_logged_in.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.FOUND
    expected_url = reverse(
        'news:detail', args=(comment.news.id,)
    ) + '#comments'
    assert response.url == expected_url
    comment.refresh_from_db()
    assert comment.text == form_data['text']
