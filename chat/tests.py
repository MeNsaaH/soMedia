""" Tests for the Chats application """
from django.test import Client, TestCase
from django.urls import reverse

from libs.tests import TestMixin

from .forms import CommentForm, PostForm
from .models import Comment, Post


class HomeTestCase(TestCase, TestMixin):
    
    def test_home_page_rendered(self):
        """ Asserts that home page is rendered with the right template and form """
        user = self._create_user_and_login('john')
        response = self.client.get(reverse('chat:home'))
        self.assertTemplateUsed(response, 'chat/home.html')
        self.assertTrue(isinstance(response.context['comment_form'], CommentForm))
        self.assertEqual(len(response.context['posts']), 0)

    def test_redirect_if_user_is_not_logged_in(self):
        """ Asserts that user is redirected if not logged in """    
        response = self.client.get(reverse('chat:home'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('chat:home')}")


class PostTestCase(TestCase, TestMixin):

    def test_post_redirect_not_logged_in(self):
        response = self.client.get(reverse('chat:add_post'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('chat:add_post')}")

    def test_view_get(self):
        user = self._create_user_and_login('john')
        response = self.client.get(reverse('chat:add_post'))
        self.assertTrue(isinstance(response.context['form'], PostForm))
        self.assertTemplateUsed('chat/add_post.html')

    def test_valid_add_post(self):
        user = self._create_user_and_login('john')
        response = self.client.post(reverse('chat:add_post'), data={'post':'new post'})
        self.assertRedirects(response, reverse('chat:home'))
        self.assertEqual(Post.objects.count(), 1)


class CommentTestCase(TestCase, TestMixin):

    def setUp(self):
        self.user = self._create_user_and_login('john')
        self._post = Post.objects.create(user=self.user, text='some new post')
        
    def test_only_post_allowed(self):
        """ Tests that only post is allowed"""
        response = self.client.get(reverse('chat:add_comment', args=(self._post.id, )))
        self.assertEqual(response.status_code, 405)
    
    def test_comment(self):
        response = self.client.post(reverse('chat:add_comment', args=(self._post.id,)), data={'text': 'new comment'})
        self.assertRedirects(response, reverse('chat:home'))
        self.assertEqual(Comment.objects.count(), 1)
        new_comment = Comment.objects.last()
        self.assertEqual(self._post, new_comment.post)
