from django import forms
from .models import Post, Comment
      

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('picture', 'text')


class CommentForm(forms.Form):
	text = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'rows': 3}))

	def save(self, post, user):
		comment = Comment.objects.create(text=self.cleaned_data.get('text', None), post=post, user=user)
		return comment