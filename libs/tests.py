from django.contrib.auth import get_user_model

User = get_user_model()

class TestMixin:

    def _create_user_and_login(self, username):
        """ create and new user and login """
        user = User.objects.create(username=username, email='john@test.com')
        user.set_password('secret')
        user.save()
        self.client.login(username='john', password='secret')
        return user

    def _create_user(self, username, password):
        """ Creates a user """
        user = User.objects.create(username=username, email='john@test.com')
        user.set_password(password)
        user.save()
        return user
