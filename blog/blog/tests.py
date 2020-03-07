from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Post

# Create your tests here.
class BlogTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testUser',
            email='test@phos.com',
            password='password'
        )

        self.post = Post.objects.create(
            title='A good title',
            body='the body content',
            author=self.user
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(),'/post/1/')

    def test_spring_representation(self):
        post = Post(title='A good title')
        self.assertEqual(str(post),post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}','A good title')
        self.assertEqual(f'{self.post.body}','the body content')
        self.assertEqual(f'{self.post.author}','testUser')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'the body content')
        self.assertTemplateUsed(response,'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code,404)
        self.assertContains(response,'the body content')
        self.assertTemplateUsed(response,'post_details.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'A new post',
            'body': 'a new body',
            'author': self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'post_new.html')
        self.assertContains(response,'a new body')
        self.assertContains(response, 'A new post')

    def test_post_update_view(self):
        response = self.client.get(reverse('post_edit', args='1'),{
            'title': 'Update title',
            'body': 'update body'
        })
        self.assertEqual(response.status_code, 200)

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete',args='1'))
        self.assertEqual(response.status_code, 200)



