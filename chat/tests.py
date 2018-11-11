""" Tests for the Chats application """

from django.test import Client, TestCase
from django.urls import reverse


# Create your tests here.
class TestHomePage(TestCase):
    
    def test_home_page_template(self):
        """ Asserts that home page is rendered with the right template """
        pass

    def test_redirect_if_user_is_not_logged_in(self):
        """ Asserts that user is redirected if not logged in """    
        pass
    
    def test_comment_form_is_rendered(self):
        """ Tests that the CommentForm is used in Rendering the HomePage """"
        pass
