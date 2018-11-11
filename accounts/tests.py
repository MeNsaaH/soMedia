from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import ProfileForm

User = get_user_model()

class LoginTestCase(TestCase):
    """ User LogIn test case"""

    def test_login_redirect_if_user_not_logged_in(self):
        """ tests login """
        response = self.client.get(reverse('chat:home'))
        self.assertRedirects(response, '/accounts/login/?next=/')

        with self.settings(LOGIN_URL='/accounts/register/'):
            response = self.client.get('')
            self.assertRedirects(response, '/accounts/register/?next=/')

    def test_login_template(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertTemplateUsed(response, 'registration/login.html')
    
    # def test_redirect_in_user_logged_in(self):
    #     User = get_user_model()
    #     new_user = User.objects.create(username='abc', email='abc@test.com')
    #     new_user.set_password('abc')
    #     self.client.login(username='abc', password='abc')
    #     response = self.client.get(reverse('accounts:login'))
    #     self.assertRedirects(response, reverse('chat:home'))


class RegistrationTestCase(TestCase):

    def test_redirect_if_user_logged_in(self):
        _user = User.objects.create(username='abc', email='abc@test.com')
        _user.set_password('abc')
        _user.save()
        self.client.login(username='abc', password='abc')
        response = self.client.get(reverse('accounts:register'))
        self.assertRedirects(response, reverse('chat:home'))

    def test_valid_registration(self):
        valid_reg_data = {
            'username': 'john',
            'email': 'john@test.com',
            'first_name': 'john',
            'last_name': 'doe',
            'password1': '@secret123',
            'password2': '@secret123'
        }
        response = self.client.post(reverse('accounts:register'), valid_reg_data)
        self.assertRedirects(response, reverse('chat:home'))
        self.assertEqual(User.objects.count(), 1)
    
    def test_invalid_registration(self):
        invalid_reg_data = [
            {
                # mismatched Passwords
                'username': 'john',
                'email': 'john@test.com',
                'first_name': 'john',
                'last_name': 'doe',
                'password1': 'secret12',
                'password2': 'secret123'
            },
            {
                # wrong Email
                'username': 'john',
                'email': 'johntest.com',
                'first_name': 'john',
                'last_name': 'doe',
                'password1': 'secret123',
                'password2': 'secret123'
            },
            {
                # Invalid Username
                'username': '!john',
                'email': 'john@test.com',
                'first_name': 'john',
                'last_name': 'doe',
                'password1': 'secret12',
                'password2': 'secret123'
            },

        ]
        for invalid_form in invalid_reg_data:
            response = self.client.post(reverse('accounts:register'), invalid_form)
            self.assertEqual(response.status_code, 200)
        

    def test_register_page_templates(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertTemplateUsed(response, 'registration/register.html')


class ProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='john', email='john@test.com')
        self.user.set_password('secret')
        self.user.save()
        self.client.login(username='john', password='secret')

    def test_redirect_if_user_not_logged_in(self):
        """ Assert that if user is redirected to login if not logged in"""
        self.client.logout()
        response = self.client.get(reverse('accounts:view-profile', args=('someUser', )))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:view-profile', args=('someUser',))}")

    def test_view_profile(self):
        """ test profile view """
        x_user = User.objects.create(username='abc', email='abc@test.com')
        
        response = self.client.get(reverse('accounts:view-profile', args=('abc', )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/users_profile.html')
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.context['user'], x_user)
        self.assertEqual(response.context['is_following'], False)

    def test_profile_edit_view(self):
        """ Test profile_edit view """
        response = self.client.get(reverse('accounts:edit_profile'))        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], ProfileForm))
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')
    
    def test_profile_edit_success(self):
        """ Test for successful profile edit """
        new_profile_data = {
            'bio': 'Testing the application',
            'phone': '39239104831',
            'website': 'https://some.website.com',
            'address': 'Memory Loc 4'
        }
        response = self.client.post(reverse('accounts:edit_profile'), new_profile_data)
        self.assertRedirects(response, reverse('accounts:view-profile', args=(self.user.username, )))
        self.user = User.objects.get(username=self.user.username)
        self.assertEqual(self.user.profile.phone,  '39239104831')
        self.assertEqual(self.user.profile.bio,  'Testing the application')
        self.assertEqual(self.user.profile.website,  'https://some.website.com')
        self.assertEqual(self.user.profile.address,  'Memory Loc 4')


class FollowerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='john', email='john@test.com')
        self.user.set_password('secret')
        self.user.save()
        self.client.login(username='john', password='secret')
        self.a_user = User.objects.create(username='a_', email='a@test.com')
        self.b_user = User.objects.create(username='b_', email='b@test.com')
        self.c_user = User.objects.create(username='c_', email='c@test.com')
        self.user.followers.add(self.a_user)

    def test_redirect_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:followers'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:followers')}")
    
    def test_followers_view(self):
        response = self.client.get(reverse('accounts:followers'))
        self.assertTemplateUsed(response, 'accounts/followers.html')
        self.assertEqual(len(response.context['users_followed']), 1)
        self.assertEqual(len(response.context['unfollowed_users']), 2)
    
    def test_add_followers_view(self):
        response = self.client.get(reverse('accounts:follow', args=('b_', )))
        self.assertRedirects(response, reverse('accounts:followers'))
        self.assertEqual(self.user.followers.count(), 2)

    def test_remove_followers_view(self):
        response = self.client.get(reverse('accounts:unfollow', args=('a_', )))
        self.assertRedirects(response, reverse('accounts:followers'))
        self.assertEqual(self.user.followers.count(), 0)
