from django.db import models
from django.conf import settings


class Post(models.Model):
	""" The Posts Models """

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
	picture = models.ImageField(upload_to='posts', blank=True)
	text = models.TextField(max_length=2048, blank=True)
	posted_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username}'s post"

class Comment(models.Model):
	""" The comments Models """

	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	text = models.TextField(max_length=2048, blank=True)
	comment_date = models.DateTimeField(auto_now_add=True)
