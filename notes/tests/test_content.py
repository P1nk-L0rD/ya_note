from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username="user")

        cls.note = Note.objects.create(
            title='Some_title',
            text='Some_text',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        users = (
            (self.author, True),
            (self.reader, False),
        )
        url = reverse('notes:list')
        for user, status in users:
            self.client.force_login(user)
            response = self.client.get(url)
            content = response.context['object_list']
            self.assertEqual((self.note in content), status)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        self.client.force_login(self.author)
        for name, args in urls:
            url = reverse(name, args=args)
            response = self.client.get(url)
            self.assertEqual(('form' in response.context), True)
