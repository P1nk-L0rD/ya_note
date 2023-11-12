from http import HTTPStatus

from pytils.translit import slugify
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestLogic(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username="user")

        # cls.note = Note.objects.create(
        #     title='Some_title',
        #     text='Some_text',
        #     author=cls.author,
        # )
        cls.form_data = {
            'title': 'Some_title',
            'text': 'Some_text',
            'slug': 'Some_title',
        }

    def test_user_can_create_note(self):
        url = reverse('notes:add')
        self.client.force_login(self.author)
        response = self.client.post(url, data=self.form_data)
        redirect_url = reverse('notes:success')
        self.assertEqual(response.url, redirect_url)
        amount_of_notes = Note.objects.count()
        self.assertEqual(amount_of_notes, 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])

