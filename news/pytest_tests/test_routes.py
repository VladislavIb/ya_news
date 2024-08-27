"""Тестирование маршрутов."""
import pytest

from http import HTTPStatus

from django.urls import reverse


@pytest.mark.parametrize(
    'name',
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
@pytest.mark.django_db
def test_home_availability_for_anonymous_user(client, name):
    """Проверка доступности главной страницы."""
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'client_fixture, expected_status',
    (
        ('client_with_author_logged_in', HTTPStatus.OK),
        ('client_with_reader_logged_in', HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_availability_for_comment_edit_and_delete(
    request, client_fixture, name, comment, expected_status
):
    """Проверка доступности редактирования и удаления комментария."""
    client = request.getfixturevalue(client_fixture)
    url = reverse(name, args=(comment.id,))
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_redirect_for_anonymous_client(client, name, comment):
    """Проверка редиректа для анонимного пользователя."""
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assert response.status_code == HTTPStatus.FOUND
    assert response.url == redirect_url
