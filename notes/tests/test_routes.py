from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username="user")

        cls.note = Note.objects.create(
            title='Some_title',
            text='Some_text',
            author=cls.author,
        )

    # def test_public_pages(self):
    #     urls = (
    #         ('notes:home', None),
    #     )

    def test_pages_availability(self):
        user_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND)
        )

        urls = (
            ('notes:detail', (self.note.slug,)),
        )

        for user, status in user_statuses:
            self.client.force_login(user)
            for name, args in urls:
                with self.subTest(name=name):
                    url = reverse(name, args=args)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)
    
    # def test_pages(self):
