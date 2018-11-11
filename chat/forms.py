from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
	""" Form for handling addition of posts """

	class Meta:
		model = Post
		fields = ('picture', 'text')


class CommentForm(forms.Form):
	""" Form for adding comments"""

	text = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'rows': 3}))

	def save(self, post, user):
		""" custom save method to create comment """

		comment = Comment.objects.create(text=self.cleaned_data.get('text', None), post=post, user=user)
