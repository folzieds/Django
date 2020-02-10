from django.test import TestCase
from django.urls import reverse
from .models import Post

# Create your tests here.
class PostModelTest(TestCase):

    def setUp(self):
        Post.objects.create(text='just a test string')

    def test_text_context(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.text}'
        self.assertEqual(expected_object_name,'just a test string')

class HomePageViewTest(TestCase):

    def setUp(self):
        Post.objects.create(text='just another string')

    def test_view_url_exists_at_proper_location(self):
        link = self.client.get('/')
        self.assertEqual(link.status_code, 200)

    def test_view_url_by_name(self):
        link = self.client.get(reverse('home'))
        self.assertEqual(link.status_code, 200)

    def test_view_uses_correct_template(self):
        link = self.client.get(reverse('home'))
        self.assertEqual(link.status_code,200)
        self.assertTemplateUsed(link,'home.html')