from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    """ Custom User Model 
        In cases where we just want to add a new field to the already existing user, subclass
        the `AbstractUser` and add the required fields
        Ensure to update the `settings.AUTH_USER_MODEL` value
    """
    followers = models.ManyToManyField("self", blank=True)

    def is_following(self, user):
        return user in self.followers.all()



class UserProfile(models.Model):
    """ Profile data of user """

    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                                related_name='profile',
                                verbose_name='other Details')
    picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=11, blank=True)
    address = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """ Create a profile anytime a new user is created """
    if kwargs['created']:
        user_profile = UserProfile.objects.get_or_create(
                                    user=kwargs['instance']
                                    )

